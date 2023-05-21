import PySimpleGUI as sg
import io
import logging
import locale
import ast
import piexif
import xlwings as xw
from PIL import Image
import create_worker_database as wb_com
import worker_payload_frontend as wb_front

'''
-----------------------------------------------------------------------------------
#* Note: Inserting Data to Database
#? QA:
#! Warning:
#TODO:
-----------------------------------------------------------------------------------
'''
def load_img(img_path):
    try:
        exif_dict = piexif.load(img_path)
        if '0th' in exif_dict and piexif.ImageIFD.Orientation in exif_dict['0th']:
            orientation = exif_dict['0th'][piexif.ImageIFD.Orientation]
            if orientation == 3:
                image = Image.open(img_path).rotate(180, expand=True)
            elif orientation == 6:
                image = Image.open(img_path).rotate(270, expand=True)
            elif orientation == 8:
                image = Image.open(img_path).rotate(90, expand=True)
            else:
                image = Image.open(img_path)
        else:
            image = Image.open(img_path)
        
        image.thumbnail((190, 250))
        bio = io.BytesIO()
        image.save(bio, format="PNG")
        return bio.getvalue()
    except Exception as e:
        sg.popup(f'Error Converting Image: {str(e)}')


def put_input_to_database(values):
    try:
        name = values['-NAME-']
        date = values['-DATE-']
        present_status = 1 if values['-P_YES-'] else 0
        money_earn = float(values['-INCOME-'])
        money_lost = float(values['-OUTCOME-'])
        note = values['-MLINE-']
        wb_com.insert_input_to_database(name, date, present_status, money_earn, money_lost, note)
        logging.info('Data has been added to the database')
    except Exception as e:
        logging.error(f'Error while adding data to the database: {e}')
        raise      
    logging.basicConfig(level=logging.INFO)


def put_image_to_database(values):
    name = values['-NAME-']
    process_image = values['-SELECT_IMG-']
    state = True
    if not process_image:
        state = not True
        sg.popup('Please select an image file')
        logging.info('Image has been inserted to the database')
    else:
        state = True
        wb_com.insert_or_update_image(name, process_image)
    return state

'''
-----------------------------------------------------------------------------------
#* Note: Get Filler Data
#? QA:
#! Warning:
#TODO:
-----------------------------------------------------------------------------------
'''
def get_cb_name(window, values):
    new_data = wb_com.get_unique_names_from_database()
    values['-SELECT_WORKER_NAME-'] = new_data
    values['-FILTER_WORKER_NAME-'] = new_data
    window['-SELECT_WORKER_NAME-'].update(values=new_data)
    window['-FILTER_WORKER_NAME-'].update(values=new_data)

def get_cb_date(name, window):
    dates = wb_com.get_date_from_worker_name(name)
    window['-SELECT_WORKER_DATE-'].update(values=dates)

def get_input_fill(window, values):
    name = values['-SELECT_WORKER_NAME-']
    date = values['-SELECT_WORKER_DATE-']
    worker_data = wb_com.populate_input_fields(name, date)
    
    #* Update the window
    window['-NAME-'].update(value=worker_data[0])
    window['-DATE-'].update(value=worker_data[1])
    if worker_data[2] == 1:
        window['-P_YES-'].update(value=True)
    else:
        window['-P_NO-'].update(value=True)
    window['-INCOME-'].update(value=str(worker_data[3]))
    window['-OUTCOME-'].update(value=str(worker_data[4]))
    window['-MLINE-'].update(value=str(worker_data[5]))

    
def get_image_fill(window, values):
    name = values['-SELECT_WORKER_NAME-']
    retrieved_image = wb_com.populate_image_field(name)
    if retrieved_image is not None:
        window['-IMAGE-'].update(data=load_img(retrieved_image[0]))
    else:
        empty_img = r'D:\Projects\Workers Payload\default_picture.jfif'
        window['-IMAGE-'].update(data=load_img(empty_img))
        msg = 'You have not yet put an image\n Please consider putting one !'
        sg.popup(msg, title='Missing Image')


def get_date(window, values):
    name = values['-NAME-']
    new_date = wb_com.get_date_from_worker_name(name)
    window['-SELECT_WORKER_DATE-'].update(values=new_date)


def get_earning(window, values):
    name = values['-NAME-']
    date = values['-DATE-']
    new_earn = wb_com.get_earning(name, date)
    window['-INCOME-'].update(new_earn)

def get_reduction(window, values):
    name = values['-NAME-']
    date = values['-DATE-']
    new_lost = wb_com.get_cut_wage(name, date)
    window['-OUTCOME-'].update(new_lost)

def get_note(window, values):
    name = values['-NAME-']
    date = values['-DATE-']
    show_note = wb_com.get_note(name, date)
    window['-MLINE-'].update(show_note)

def get_table_content(window):
    worker_data = wb_com.get_table_content()
    table_data = [list(row) for row in worker_data]
    window['-VIEW_TABLE-'].update(table_data)
    return worker_data


def filter_table_content(window, values):
    name = values['-FILTER_WORKER_NAME-']
    month = values['-FILTER_WORKER_MONTH-']
    if name or month:
        filter_content = wb_com.get_table_filter(name, month)
        table_data = [list(row) for row in filter_content]
        window['-VIEW_TABLE-'].update(table_data)
    else:
        sg.popup('You filtered nothing lol', 'Empty Filter Warning')

            
def put_image_to_frame(values, window):
    default_image = r'D:\Projects\Workers Payload\intro_image.jfif'
    try:
        window['-IMAGE-'].update(load_img(values['-SELECT_IMG-']))
    except Exception as e:
        window['-IMAGE-'].update(load_img(default_image))
        sg.popup_error(f"Error: {e}")
           
'''
-----------------------------------------------------------------------------------
#* Note: Edit Data
#? QA:
#! Warning:
#TODO:
-----------------------------------------------------------------------------------
'''
def edit_name(window, values):
    old_name = values['-NAME-']
    new_name = sg.popup_get_text('Enter new worker name:',
                                 default_text=values['-NAME-'])
    try:
        if new_name is None:
            raise ValueError("No name is entered")
        wb_com.edit_worker_name(new_name, old_name)
        values['-NAME-'] = new_name
        window['-NAME-'].update(new_name)
    except ValueError:
        values['-NAME-'] = old_name


def edit_date(window,values):
    layout = wb_front.popup_get_calendar()
    popup_window = sg.Window('Replace Date', layout)
    event, new_values = popup_window.read()
    if event == '-OK_DATE-':
        new_date = new_values['-NEW_DATE-']
        name = values['-NAME-']
        old_date = values['-DATE-']
        wb_com.edit_worker_date(name, old_date, new_date)
        window['-DATE-'].update(new_date)
        sg.popup('Date has been Changed')
        
        
def edit_status(window, values):
    #* Get the state of the radio button
    status = 1 if values['-P_YES-'] else 0
    #* Method component
    name = values['-NAME-']
    date = values['-DATE-']
    #* Commit changes to the database
    wb_com.edit_worker_status(name, date, status)
    window['-P_YES-'].update(value=status)
    window['-P_NO-'].update(value=1-status)
    sg.popup('Status has been Updated')


#* This is such a horibble method lols
def edit_earning(values):
    name = values['-NAME-']
    date = values['-DATE-']
    new_earning = sg.popup_get_text('Edit Earning: ',
                                        default_text=values['-INCOME-'])
    try:
        if new_earning is None:
            raise ValueError("No value is changed to a valid ones")
        new_earning = float(new_earning)
        wb_com.edit_money_earn(name, date, new_earning)
        sg.popup('Earning has been updated')
    except ValueError:
        sg.popup('Operation Cancelled')

        
def edit_lost(values):
    name = values['-NAME-']
    date = values['-DATE-']
    new_cut = sg.popup_get_text('Edit Reduction: ',
                                default_text=values['-OUTCOME-'])
    try:
        if new_cut is None:
            raise ValueError("No value is changed")
        new_cut = float(new_cut)
        wb_com.edit_money_lost(name, date, new_cut)
        sg.popup('Wage cut has been updated')
    except ValueError:
        sg.popup('Operation has been cancelled')
        

def edit_note(values):
    name = values['-NAME-']
    date = values['-DATE-']
    note = values['-MLINE-']
    wb_com.edit_note(name, date, note)    

     
'''
-----------------------------------------------------------------------------------
#* Note: Clearing input
#? QA:
#! Warning:
#TODO:
-----------------------------------------------------------------------------------
'''    
def clear_user_input(window):
    window['-NAME-'].update('')
    window['-DATE-'].update('')
    window['-INCOME-'].update('')
    window['-OUTCOME-'].update('')
    window['-P_YES-'].update(value=False)
    window['-P_NO-'].update(value=False)
    window['-MLINE-'].update('')

'''
-----------------------------------------------------------------------------------
#* Note: Deletion Method
#? QA:
#! Warning: lot's of tantrum in a single line
#TODO:
-----------------------------------------------------------------------------------
'''
def delete_entry(values):
    name = values['-SELECT_WORKER_NAME-']
    date = values['-SELECT_WORKER_DATE-']
    try:
        wb_com.delete_worker_data(name, date)
    except Exception as e:
        sg.popup('You selected nothing')


def instant_deletion(values):
    name = values['-SELECT_WORKER_NAME-']
    try:
        if name is not None:
            wb_com.instant_delete(name)
            sg.popup(f'{name} has been removed')
    except Exception as e:
        sg.popup(f'Error: {e}')        

'''
-----------------------------------------------------------------------------------
#* Note: Operator View
#? QA:
#! Warning:
#TODO:
-----------------------------------------------------------------------------------
''' 
def calculate_total_earn(window, values):
    name = values['-FILTER_WORKER_NAME-']
    month = values['-FILTER_WORKER_MONTH-']
    if name or month:
        filter_content = wb_com.get_table_filter(name, month)
        total_earn = sum(float(row[3].replace('Rp. ', '').replace('.', '').replace(',', '').replace(' ', '')) for row in filter_content)
        formatted_total_earn = "Rp.{:,.0f}".format(total_earn).replace(",", ".")
        window['-SHOW_INCOME-'].update(formatted_total_earn)
    else:
        sg.popup('Only available using filter function')

        
def calculate_total_lost(window, values):
    name = values['-FILTER_WORKER_NAME-']
    month = values['-FILTER_WORKER_MONTH-']
    if name or month:
        filter_content = wb_com.get_table_filter(name, month)
        total_lost = sum(float(row[4].replace('Rp. ', '').replace('.', '').replace(',', '').replace(' ', '')) for row in filter_content)
        formatted_total_lost = "Rp.{:,.0f}".format(total_lost).replace(",", ".")
        window['-SHOW_OUTCOME-'].update(formatted_total_lost)
    else:
        sg.popup('Only available using filter function')


def calculate_total_money(window, values):
    name = values['-FILTER_WORKER_NAME-']
    month = values['-FILTER_WORKER_MONTH-']
    if name or month:
       filter_content = wb_com.get_table_filter(name, month)
       total_get = sum(float(row[3].replace('Rp. ', '').replace('.', '').replace(',', '').replace(' ', '')) for row in filter_content)
       total_lost = sum(float(row[4].replace('Rp. ', '').replace('.', '').replace(',', '').replace(' ', '')) for row in filter_content)
       total_earn = total_get - total_lost
       formatted_total_earn = "Rp.{:,.0f}".format(total_earn).replace(",",".")
       window['-TOTAL_EARN-'].update(formatted_total_earn)
    else:
        sg.popup('Not available')
       
       
def evaluate_expression(expression):
    try:
        expression = expression.strip()
        if expression.startswith('='):
            expression = expression[1:]
        node = ast.parse(expression, mode='eval')
        compiled_expr = compile(node, filename='<string>', mode='eval')
        evaluated = eval(compiled_expr, {}, {})
        return evaluated
    except Exception as e:
        print(f"Error evaluating expression: {e}")
        return None
    

def calculate_total_presense(window, values):
    name = values['-FILTER_WORKER_NAME-']
    month = values['-FILTER_WORKER_MONTH-']
    if name or month:
        filter_content = wb_com.get_table_filter(name, month)
        total_attendance = sum(1 for row in filter_content if row[2]==1)
        total_presence = sum(1 for row in filter_content if row[2] in [0,1])
        msg = f'{total_attendance}/{total_presence}'
        window['-TOTAL_PRESENCE-'].update(msg)
    else:
        msg = 'No data aquired'
        window['-TOTAL_PRESENCE-'].update(msg)


'''
-----------------------------------------------------------------------------------
#* Note: Export + View Command
#? QA:
#! Warning:
#TODO:
-----------------------------------------------------------------------------------
''' 
def export_data(wb, filename):
    locale.setlocale(locale.LC_ALL, 'id_ID')
    data = wb_com.get_export_data()
    
    # #* Launch new excel app
    sheet = wb.sheets[0]
    
    #* Write data to the worksheet
    sheet.range('A1').value = data
    
    #* Set the number format for date
    sheet.range('B:B').number_format = 'mm-dd-yyyy'
    
    #* Set the currency number formatting
    sheet.range('D:E').number_format = f'Rp #,##0.00'
    
    #* Apply coloring to worksheet
    sheet.range('A1').expand('right').api.AutoFilter(1)
    
    #* Apply border to cells
    last_row = sheet.range('A' + str(sheet.cells.last_cell.row)).end('up').row
    last_column = sheet.range('A1').end('right').column
    sheet.range('A1', sheet.cells(last_row, last_column)).api.Borders.LineStyle = 1
    
    #* Centering the content
    range_to_center = sheet.range('A1', sheet.cells(last_row, last_column))
    range_to_center.api.HorizontalAlignment = xw.constants.HAlign.xlHAlignCenter
    range_to_center.api.VerticalAlignment = xw.constants.VAlign.xlVAlignCenter
    
                 
    #* Fit cell's content
    sheet.range('A:A').column_width = 15
    sheet.range('B:B').column_width = 15
    sheet.range('C:C').column_width = 15
    sheet.range('D:D').column_width = 25
    sheet.range('E:E').column_width = 25
    sheet.range('F:F').column_width = 40
    
    #* Save the workbook
    wb.save(filename)
    
    #* Close and quit the app
    wb.close()


def view_file(values):
    try:
        file_name = values['-FILE_DIR-']
        if file_name:
            wb = xw.Book(file_name)
            wb.app.visible = True
            wb.app.activate()
            wb.app.api.WindowState = -4137
        else:
            sg.popup('Sorry, File is not valid')
    except Exception as e:
        sg.popup(f'Error: {e}')


def export_file():
    message = 'Export to:'
    export_format = (("Excel File (2007, Above)", ".xlsx"),
                     ("Excel File (97-2003)", ".xls"),
                     ("CSV", ".csv"))
    file_name = sg.popup_get_file(message, 'Export', save_as=True, file_types=export_format)
    if file_name:
        with xw.App(visible=False) as app:
            wb = app.books.add()
            export_data(wb, file_name)
    else:
        sg.popup('Operation has been cancelled')


def app_info_msg():
    filename = r'D:\Projects\Workers Payload\App_info.txt'
    try:
        with open(filename, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"{filename} doesn not exist")
        return None
    except IOError:
        print(f"Error Reading {filename}")
        return None        


'''
-----------------------------------------------------------------------------------
#* Note: Main Program Loop
#? QA:
#! Warning:
#TODO:
-----------------------------------------------------------------------------------
'''
def main_program():
    main_layout = wb_front.main_window()
    #* Event_handling
    window = sg.Window('Worker App Design', main_layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        
        
        elif event == '-ADD_DATA-':
            put_input_to_database(values)
            get_cb_name(window, values)
            get_table_content(window)
            sg.popup_notify('Data has been added', 'Message', display_duration_in_ms=1000)
        
        
        elif event == '-EDIT_IMG-':
            set_img = put_image_to_database(values)
            if set_img is True:
                window['-IMAGE-'].update(load_img(values['-SELECT_IMG-']))
                sg.popup('Picture has been updated')
            else:
                default_img = r'D:\Projects\Workers Payload\intro_image.jfif'
                window['-IMAGE-'].update(load_img(default_img))
     

        elif event == '-SELECT_WORKER_NAME-':
            worker_name = values['-SELECT_WORKER_NAME-']
            get_cb_date(worker_name, window)

        
        elif event == '-SELECT_WORKER_DATE-':
            get_input_fill(window, values)
            get_image_fill(window, values)
        
        
        elif event == '-DISPLAY-':
            put_image_to_frame(values, window)
            
        
        elif event == '-EDIT_NAME-':
            edit_name(window, values)
            get_cb_name(window, values)
            get_table_content(window)
        
        
        elif event == '-CALC_PAY-' and values['-INCOME-']:
            expression = values['-INCOME-']
            if expression.startswith('='):
                result = evaluate_expression(expression[1:])
                if result is not None:
                    window['-INCOME-'].update(str(result))


        elif event == '-CALC_PENALTY-' and values['-OUTCOME-']:
            expression = values['-OUTCOME-']
            if expression.startswith('='):
                result = evaluate_expression(expression[1:])
                if result is not None:
                    window['-OUTCOME-'].update(str(result))

             
        elif event == '-EDIT_DATE-':
                edit_date(window, values)
                get_date(window, values)
                get_table_content(window)


        elif event == '-EDIT_PRESENT-':
            edit_status(window, values)
            get_table_content(window)    
        
        
        elif event == '-EDIT_PAY-':
            edit_earning(values)
            get_earning(window, values)
            get_table_content(window)        
            
            
        elif event == '-EDIT_PENALTY-':
            edit_lost(values)
            get_reduction(window, values)
            get_table_content(window)            
        
            
        elif event == '-EDIT_NOTE-':
            edit_note(values)
            get_note(window, values)
            
        
        elif event == '-FILTER-':
            filter_table_content(window, values)
            calculate_total_earn(window, values)
            calculate_total_lost(window, values)
            calculate_total_money(window, values)
            calculate_total_presense(window, values)


        elif event == '-SHOW_ALL-':
            get_table_content(window)
            window['-SHOW_INCOME-'].update(value='')
            window['-SHOW_OUTCOME-'].update(value='')
            window['-TOTAL_EARN-'].update(value='')
            
            
        elif event == '-CLEAR_INPUT-':
            clear_user_input(window)
            default_img = r'D:\Projects\Workers Payload\intro_image.jfif'
            window['-IMAGE-'].update(load_img(default_img))


        elif event == '-DELETE-':
            delete_entry(values)
            get_cb_name(window, values)
            get_date(window, values)
            get_table_content(window)
            clear_user_input(window)
            default_img = r'D:\Projects\Workers Payload\intro_image.jfif'
            window['-IMAGE-'].update(load_img(default_img))
            sg.popup_notify('Data has been removed', '(Warning Message)', icon=sg.SYSTEM_TRAY_MESSAGE_ICON_WARNING, display_duration_in_ms=100)


        elif event == '-INSTANT_DELETE-':
            instant_deletion(values)
            get_cb_name(window, values)
            get_date(window, values)
            get_table_content(window)
            clear_user_input(window)
            default_img = r'D:\Projects\Workers Payload\intro_image.jfif'
            window['-IMAGE-'].update(load_img(default_img))
            sg.popup_notify('Entire Named Data has been removed', '(Warning Message)', icon=sg.SYSTEM_TRAY_MESSAGE_ICON_WARNING, display_duration_in_ms=100)            


        elif event == '-EXPORT-':
            export_file()
            sg.popup('You Have Exported the Database Content')


        elif event == '-VIEW_FILE-':
            view_file(values)

            
        elif event == '-APP_INFO-':
            msg = app_info_msg()
            sg.popup_scrolled(msg, 'App Info')


'''
-----------------------------------------------------------------------------------
#* Note: Main method launch
#? QA:
#! Warning:
#TODO:
-----------------------------------------------------------------------------------
'''            
if __name__ == '__main__':
    main_program()