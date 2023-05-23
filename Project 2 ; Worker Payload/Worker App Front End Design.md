This is not divide directly like the database or back end since PySimpleGUI is really a straight foward system
#### Part 0: Import and Initial settings
```python
import PySimpleGUI as sg
import create_worker_database as wb_com
import worker_payload_backend as wb_end

sg.theme('DarkTeal6')
```

#### Part 1: Input Interface
This one's pretty standard. The noteworthy section is the `sg.Column()` usage on `layout_3`.
```python
def input_interface():
    accepted_files = (("JPEG File", ".jpg"),
                      ("PNG File", ".png"),
                      ("BIMP File", ".bmp"),
                      ("SVG File", ".svg"),
                      )
    # Set the default image to a camera or something
    default_img = r'D:\Projects\Workers Payload\intro_image.jfif'
    
    # Layout 1: Image Column
    layout_1 = [
	    [sg.Image(key='-IMAGE-',
					  # Initial Sources is required
	                  source=wb_end.load_img(default_img),
	                  size=(190, 190),
	                  tooltip='Profile Image',
	                  enable_events=True)],
	    [sg.FileBrowse('Browse Image', 
                       key='-SELECT_IMG-',
                       file_types=accepted_files,
                       enable_events=True,
                       size=(12,1), pad=((5,7),(10,10))),
         sg.Button('Show', k='-DISPLAY-', size=(10,1), pad=((3,4),(10,10)), use_ttk_buttons=True),],
		 [sg.Button('Add/Edit Image', key='-EDIT_IMG-', use_ttk_buttons=True,
		   size=(26,1), pad=((5,10),(5,5))),],
    ]
    
    # Layout 2: Input Column
    layout_2 = [
	    [sg.T('Name / Title:',
	              pad=((3,0),(0,10))),
	        sg.Input(key='-NAME-',
	                 size=(20,1),
	                pad=((55,0),(0,10))),
	        sg.Button('Edit', key='-EDIT_NAME-',
	                size=(7,1), pad=((12,1),(0,10)), use_ttk_buttons=True)],
	    
	    [sg.T('Date (dd-mm--yyyy):',
              pad=((3,0),(10,10))),
        sg.Input(size=(20,1), key='-DATE-', pad=((10,0),(10,10))),
        sg.CalendarButton('Date',
                        target='-DATE-',
                        size=(7,1),
                        format='%d-%m-%Y',
                        pad=((10,0),(10,10))),
        sg.Button('Edit', k='-EDIT_DATE-',
                  size=(7,1), use_ttk_buttons=True)],
        
        [sg.T('Present Status:',
              pad=((3,0),(10,10))),
        sg.Radio('Present', group_id='-STATUS-', key='-P_YES-', pad=((35,0),(10,10))),
        sg.Radio('Absent', group_id='-STATUS-', key='-P_NO-', pad=((10,0),(10,10))),
        sg.Button('Edit', key='-EDIT_PRESENT-',
                  size=(7,1), pad=((7,0),(10,10)), use_ttk_buttons=True)],
        
        [sg.T('Payment (daily): ',
              pad=((3,0),(10,10))),
        sg.Input(size=(20,1), pad=((30,0),(10,10)), key='-INCOME-', enable_events=True),
        sg.Button('Calc', key='-CALC_PAY-',
                  size=(7,1), pad=((10,0),(10,10)), use_ttk_buttons=True),
        sg.Button('Edit', key='-EDIT_PAY-',
                  size=(7,1), pad=((10,0),(10,10)), use_ttk_buttons=True)],
        
        [sg.T('Penalty (daily): ',
              pad=((2,0),(10,10))),
        sg.Input(size=(20,1), pad=((38,0),(10,10)), key='-OUTCOME-', enable_events=True),
        sg.Button('Calc', key='-CALC_PENALTY-',
                  size=(7,1), pad=((10,0),(10,10)), use_ttk_buttons=True),
        sg.Button('Edit', key='-EDIT_PENALTY-',
                  size=(7,1), pad=((10,0),(10,10)), use_ttk_buttons=True)],
        
        [sg.T('Work Done:',
              pad=((2,0),(5,90))),
         sg.Multiline(size=(30,6), 
                      key='-MLINE-',
                      pad=((58,0),(10,10))),
         sg.Button('Edit', key='-EDIT_NOTE-',
                   size=(7,1), pad=((10,0),(0,10)), use_ttk_buttons=True)],
        
    ]
    
    #* Layout 3: Column and segmented result
    layout_3 = [
        [sg.Column(layout_1),
        sg.Column(layout_2)]
    ]
    
    return layout_3
```

#### Part 2: Edit / Filter Interface
```python
def edit_interface():
	tooltip_list = ['Select Worker Name',
                    'Select Date',
                    'Single Deletion Method',
                    'Instant Object Removal']
    
    layout_4 = [
	    [sg.T('Worker Name:'), 
         sg.Combo(values=wb_com.get_unique_names_from_database(),
                  enable_events=True,
                  size=(20,1),
                  key='-SELECT_WORKER_NAME-',
                  tooltip=tooltip_list[0],)],
              
        [sg.T('Date:'), 
         sg.Combo(values=[],
                  enable_events=True,
                  size=(20,1),
                  key='-SELECT_WORKER_DATE-',
                  pad=((58, 0),(0, 0)),
                  tooltip=tooltip_list[1])],
        
        [sg.Button('Delete', key='-DELETE-', size=(15,1), pad=((10, 10),(10, 10)), 
                   use_ttk_buttons=True, tooltip=tooltip_list[2]),
         sg.Button('Instant Delete', key='-INSTANT_DELETE-', size=(15,1), pad=((10, 10),(10, 10)), 
                   use_ttk_buttons=True, tooltip=tooltip_list[3])],
    ]
    
    return layout_4
```

#### Part 3: Action Interface
```python
# Action would consist of export, add, and view
def action_interface():
	layout = [
		[sg.T('Select File:'), 
	         sg.Input(size=(30,1), k='-FILE_DIR-'),
	         sg.FileBrowse(target='-FILE_DIR-')],
	    
	    [sg.Button('Export Data', key='-EXPORT-',
                   size=(10,1), pad=((10,0),(20,10)), use_ttk_buttons=True),
         sg.Button('Clear Window', key='-CLEAR_INPUT-',
                   size=(12,1), pad=((15,0),(20,10)), use_ttk_buttons=True),
         sg.Button('Add', key='-ADD_DATA-',
                   size=(8,1), pad=((15,0),(20,10)), use_ttk_buttons=True),
         sg.Button('View', size=(7,1),
                   key='-VIEW_FILE-', pad=((10,0),(20,10)), use_ttk_buttons=True)],
	]
	
	return layout_6
```

#### Part 4: Input Interface Tab Assembly
The most important thing is the layouting of the `sg.Frame()`
```python
# Interface
def first_interface():
	quick_edit_tab = edit_interface()
	quick_action_tab = action_interface()
	input_tab = input_interface()
	input_tab_layout = [
		[sg.Frame('Edit', quick_edit_tab, pad=((20,10), (10,0))), 
         sg.Frame('Action', quick_action_tab, pad=((10,20),(10,0))),],
        [sg.Frame('Input', input_tab, pad=((20,20),(20,20)))],
	]
```

#### Part 5: View Tab
```python
def view_interface():
	worker_heading = ['Name', 'Date', 'Present Status', 'Earning', 'Wage Cut']
	# List to be inserted in Month ComboBox
	month_nums = [str(i) for i in range(1,13)]
	
	layout_7 = [
		[sg.T('Name:'),
         sg.Combo(values=wb_com.get_unique_names_from_database(),
                  enable_events=True,
                  size=(20,1),
                  key='-FILTER_WORKER_NAME-',
                  tooltip='Select Worker Name'),
         sg.T('Month:'),
         sg.Combo(values=month_nums,
                  enable_events=True,
                  size=(20,1),
                  k='-FILTER_WORKER_MONTH-',
                  tooltip='Select Worker Name',
                  pad=((0, 0),(0, 0)),),
         sg.Button('Filter', k='-FILTER-', pad=((10,5),(5,0)), use_ttk_buttons=True),
         sg.Button('Show All', k='-SHOW_ALL-', pad=((10,10),(5,0)), use_ttk_buttons=True),
         sg.Button('App Info', k='-APP_INFO-', pad=((10,0),(5,0)), use_ttk_buttons=True)],
         
        [sg.T('')],
        [sg.HorizontalSeparator()],
        
        [sg.Table(values = wb_com.get_table_content(),
                  headings=worker_heading,
                  auto_size_columns=False,
                  col_widths = [15, 12, 12, 14, 14],
                  pad=((50,20),(20,20)),
                  k='-VIEW_TABLE-',
                  vertical_scroll_only=False,
                  justification = 'center',
                  enable_events=True)],
        
        [sg.HorizontalSeparator()],
        [sg.T('Filtered Result', font='Default 11')],
        [sg.T('Income Sum:', 
              font='Default 10'), 
         sg.Input(size=(25,1), 
                  k='-SHOW_INCOME-',
                  pad=((37, 0),(0, 0)))],
        [sg.T('Reduction Sum:', 
              font='Default 10'),
         sg.Input(size=(25,1), 
                  k='-SHOW_OUTCOME-',
                  pad=((20, 0),(0, 0)))],
        [sg.T('Total Earn:'),
         sg.Input(size=(25,1), 
                  key='-TOTAL_EARN-',
                  pad=((50,0),(0,0)))],
        [sg.T('Total Presence:'),
         sg.Input(size=(25,1),
                  key='-TOTAL_PRESENCE-',
                  pad=((21,0),(0,0)))]
	]
	
	return layout_7
```

#### Part 6: Custom Popup Layout
```python
def popup_get_calendar():
	layout = [
        [sg.T('Select New Date:'),],
        [sg.Input(key='-NEW_DATE-', size=(15,1)),
         sg.CalendarButton('Date',
                        target='-NEW_DATE-',
                        size=(7,1),
                        format='%d-%m-%Y',
                        pad=((10,0),(10,10)))],
        [sg.Button('Save',k='-OK_DATE-')],
    ]
    return layout
```

#### Part 7: Main Window
```python
def main_window():
	tab_1 = first_interface()
	tab_2 = view_interface()
	tab_layout = [[sg.Tab('Input', tab_1)],
                  [sg.Tab('View', tab_2)]]
    main_layout = [[sg.TabGroup(tab_layout)]]
    return main_layout
```

#### Part 8: Full VS Source
```python
import PySimpleGUI as sg
import create_worker_database as wb_com
import worker_payload_backend as wb_end

sg.theme('DarkTeal6')

'''
-----------------------------------------------------------------------------------
#* Note: Input Interface
#? QA:
#! Warning:
#TODO:
-----------------------------------------------------------------------------------
'''

def input_interface():
    #* Image selector
    #TODO: Padding
    accepted_files = (("JPEG File", ".jpg"),
                      ("PNG File", ".png"),
                      ("BIMP File", ".bmp"),
                      ("SVG File", ".svg"),
                      )
    
    default_img = r'D:\Projects\Workers Payload\intro_image.jfif'

    #* Layout goes here
    layout_1 = [
        [sg.Image(key='-IMAGE-',
                  source=wb_end.load_img(default_img),
                  size=(190, 190),
                  tooltip='Profile Image',
                  enable_events=True)],
        [sg.FileBrowse('Browse Image', 
                       key='-SELECT_IMG-',
                       file_types=accepted_files,
                       enable_events=True,
                       size=(12,1), pad=((5,7),(10,10))),
         sg.Button('Show', k='-DISPLAY-', size=(10,1), pad=((3,4),(10,10)), use_ttk_buttons=True),],
        [sg.Button('Add/Edit Image', key='-EDIT_IMG-', use_ttk_buttons=True,
                   size=(26,1), pad=((5,10),(5,5))),],
    ]
    
    #* Edit/append data
    layout_2 = [
        [sg.T('Name / Title:',
              pad=((3,0),(0,10))),
        sg.Input(key='-NAME-',
                 size=(20,1),
                pad=((55,0),(0,10))),
        sg.Button('Edit', key='-EDIT_NAME-',
                size=(7,1), pad=((12,1),(0,10)), use_ttk_buttons=True)],
        
        [sg.T('Date (dd-mm--yyyy):',
              pad=((3,0),(10,10))),
        sg.Input(size=(20,1), key='-DATE-', pad=((10,0),(10,10))),
        sg.CalendarButton('Date',
                        target='-DATE-',
                        size=(7,1),
                        format='%d-%m-%Y',
                        pad=((10,0),(10,10))),
        sg.Button('Edit', k='-EDIT_DATE-',
                  size=(7,1), use_ttk_buttons=True)],
        
        [sg.T('Present Status:',
              pad=((3,0),(10,10))),
        sg.Radio('Present', group_id='-STATUS-', key='-P_YES-', pad=((35,0),(10,10))),
        sg.Radio('Absent', group_id='-STATUS-', key='-P_NO-', pad=((10,0),(10,10))),
        sg.Button('Edit', key='-EDIT_PRESENT-',
                  size=(7,1), pad=((7,0),(10,10)), use_ttk_buttons=True)],
        
        [sg.T('Payment (daily): ',
              pad=((3,0),(10,10))),
        sg.Input(size=(20,1), pad=((30,0),(10,10)), key='-INCOME-', enable_events=True),
        sg.Button('Calc', key='-CALC_PAY-',
                  size=(7,1), pad=((10,0),(10,10)), use_ttk_buttons=True),
        sg.Button('Edit', key='-EDIT_PAY-',
                  size=(7,1), pad=((10,0),(10,10)), use_ttk_buttons=True)],
        
        [sg.T('Penalty (daily): ',
              pad=((2,0),(10,10))),
        sg.Input(size=(20,1), pad=((38,0),(10,10)), key='-OUTCOME-', enable_events=True),
        sg.Button('Calc', key='-CALC_PENALTY-',
                  size=(7,1), pad=((10,0),(10,10)), use_ttk_buttons=True),
        sg.Button('Edit', key='-EDIT_PENALTY-',
                  size=(7,1), pad=((10,0),(10,10)), use_ttk_buttons=True)],
        
        [sg.T('Work Done:',
              pad=((2,0),(5,90))),
         sg.Multiline(size=(30,6), 
                      key='-MLINE-',
                      pad=((58,0),(10,10))),
         sg.Button('Edit', key='-EDIT_NOTE-',
                   size=(7,1), pad=((10,0),(0,10)), use_ttk_buttons=True)],
        
    ]
    
    #* Layout 3: Column and segmented result
    layout_3 = [
        [sg.Column(layout_1),
        sg.Column(layout_2)]
    ]
    
    return layout_3

'''
-----------------------------------------------------------------------------------
#* Note: Edit Interface
#? QA:
#! Warning:
#TODO:
-----------------------------------------------------------------------------------
'''
def edit_interface():

    tooltip_list = ['Select Worker Name',
                    'Select Date',
                    'Single Deletion Method',
                    'Instant Object Removal']
 
    layout_4 = [
        [sg.T('Worker Name:'), 
         sg.Combo(values=wb_com.get_unique_names_from_database(),
                  enable_events=True,
                  size=(20,1),
                  key='-SELECT_WORKER_NAME-',
                  tooltip=tooltip_list[0],)],
        
        [sg.T('Date:'), 
         sg.Combo(values=[],
                  enable_events=True,
                  size=(20,1),
                  key='-SELECT_WORKER_DATE-',
                  pad=((58, 0),(0, 0)),
                  tooltip=tooltip_list[1])],
        
        [sg.Button('Delete', key='-DELETE-', size=(15,1), pad=((10, 10),(10, 10)), 
                   use_ttk_buttons=True, tooltip=tooltip_list[2]),
         sg.Button('Instant Delete', key='-INSTANT_DELETE-', size=(15,1), pad=((10, 10),(10, 10)), 
                   use_ttk_buttons=True, tooltip=tooltip_list[3])],
    ]
    
    return layout_4

'''
-----------------------------------------------------------------------------------
#* Note: Action Interface
#? QA:
#! Warning:
#TODO:
-----------------------------------------------------------------------------------
'''
def action_interface():
    layout_6=[
        [sg.T('Select File:'), 
         sg.Input(size=(30,1), k='-FILE_DIR-'),
         sg.FileBrowse(target='-FILE_DIR-')],
        
        [sg.Button('Export Data', key='-EXPORT-',
                   size=(10,1), pad=((10,0),(20,10)), use_ttk_buttons=True),
         sg.Button('Clear Window', key='-CLEAR_INPUT-',
                   size=(12,1), pad=((15,0),(20,10)), use_ttk_buttons=True),
         sg.Button('Add', key='-ADD_DATA-',
                   size=(8,1), pad=((15,0),(20,10)), use_ttk_buttons=True),
         sg.Button('View', size=(7,1),
                   key='-VIEW_FILE-', pad=((10,0),(20,10)), use_ttk_buttons=True)],
    ]
    
    return layout_6

def first_interface():
    quick_edit_tab = edit_interface()
    quick_action_tab = action_interface()
    input_tab = input_interface()
    input_tab_layout = [
        [sg.Frame('Edit', quick_edit_tab, pad=((20,10), (10,0))), 
         sg.Frame('Action', quick_action_tab, pad=((10,20),(10,0))),],
        [sg.Frame('Input', input_tab, pad=((20,20),(20,20)))],
    ]

    return input_tab_layout

'''
-----------------------------------------------------------------------------------
#* Note: View Interface
#? QA:
#! Warning:
#TODO:
-----------------------------------------------------------------------------------
'''
def view_interface():
    #* Table Heading
    worker_heading = ['Name', 'Date', 'Present Status', 'Earning', 'Wage Cut']
    #* List of month names
    month_nums = [str(i) for i in range(1,13)]

    layout_7 = [
        [sg.T('Name:'),
         sg.Combo(values=wb_com.get_unique_names_from_database(),
                  enable_events=True,
                  size=(20,1),
                  key='-FILTER_WORKER_NAME-',
                  tooltip='Select Worker Name'),
         sg.T('Month:'),
         sg.Combo(values=month_nums,
                  enable_events=True,
                  size=(20,1),
                  k='-FILTER_WORKER_MONTH-',
                  tooltip='Select Worker Name',
                  pad=((0, 0),(0, 0)),),
         sg.Button('Filter', k='-FILTER-', pad=((10,5),(5,0)), use_ttk_buttons=True),
         sg.Button('Show All', k='-SHOW_ALL-', pad=((10,10),(5,0)), use_ttk_buttons=True),
         sg.Button('App Info', k='-APP_INFO-', pad=((10,0),(5,0)), use_ttk_buttons=True)],
        
        [sg.T('')],
        [sg.HorizontalSeparator()],
        
        [sg.Table(values = wb_com.get_table_content(),
                  headings=worker_heading,
                  auto_size_columns=False,
                  col_widths = [15, 12, 12, 14, 14],
                  pad=((50,20),(20,20)),
                  k='-VIEW_TABLE-',
                  vertical_scroll_only=False,
                  justification = 'center',
                  enable_events=True)],
        
        [sg.HorizontalSeparator()],
        [sg.T('Filtered Result', font='Default 11')],
        [sg.T('Income Sum:', 
              font='Default 10'), 
         sg.Input(size=(25,1), 
                  k='-SHOW_INCOME-',
                  pad=((37, 0),(0, 0)))],
        [sg.T('Reduction Sum:', 
              font='Default 10'),
         sg.Input(size=(25,1), 
                  k='-SHOW_OUTCOME-',
                  pad=((20, 0),(0, 0)))],
        [sg.T('Total Earn:'),
         sg.Input(size=(25,1), 
                  key='-TOTAL_EARN-',
                  pad=((50,0),(0,0)))],
    ]
    return layout_7

'''
-----------------------------------------------------------------------------------
#* Note: Date Changing Custom Window
#? QA:
#! Warning:
#TODO:
-----------------------------------------------------------------------------------
'''
#* Custom calendar layout
def popup_get_calendar():
    layout = [
        [sg.T('Select New Date:'),],
        [sg.Input(key='-NEW_DATE-', size=(15,1)),
         sg.CalendarButton('Date',
                        target='-NEW_DATE-',
                        size=(7,1),
                        format='%d-%m-%Y',
                        pad=((10,0),(10,10)))],
        [sg.Button('Save',k='-OK_DATE-')],
    ]
    return layout

'''
-----------------------------------------------------------------------------------
#* Note: Main Window
#? QA:
#! Warning:
#TODO:
-----------------------------------------------------------------------------------
'''
def main_window():
    tab_1 = first_interface()
    tab_2 = view_interface()
    tab_layout = [[sg.Tab('Input', tab_1)],
                  [sg.Tab('View', tab_2)]]
    main_layout = [[sg.TabGroup(tab_layout)]]
    return main_layout
```



This is quite straight foward since front end design is easier than actually making the whole thing works
