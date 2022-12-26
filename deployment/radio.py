# ## EXPERIMENTING
# # Radio button function to selection image url or ask user for custom url for prediction
# def radio_button_function():
#     # Create a radio button for each option (empty string to hide first radio button)
#     selected_option = st.radio('Choose an option for prediction:',
#                               ('', 'Knife', 'Fork', 'Spoon', 'Cup', 'Glass', 'Plate'),
#                               index=0, key='radio_button')

#     # Set the default URL for each option
#     url_map = {
#         '': None,
#         'Knife': 'https://m.media-amazon.com/images/I/71FtjejRbvL._AC_UL320_.jpg',
#         'Fork': 'https://m.media-amazon.com/images/I/51j88-h2NZL.jpg',
#         'Spoon': 'https://m.media-amazon.com/images/I/51Dvu6GiM8L._AC_UL320_.jpg',
#         'Cup': 'https://m.media-amazon.com/images/I/61Bq3L4gbSL._AC_UL320_.jpg',
#         'Glass': 'https://m.media-amazon.com/images/I/81B88+ZiRIL._AC_UL320_.jpg',
#         'Plate': 'https://m.media-amazon.com/images/I/A14F1QVaPNL._AC_UL320_.jpg'
#     }

#     # Default URL for the selected option
#     url = url_map[selected_option]

#     # Add a reset button to return the radio button to its initial state
#     if st.button('Reset'):
#         selected_option = None

#     # Display the selected option
#     if selected_option:
#         st.write(f'You selected the option: {selected_option}')

#     return url


# # Call the radio funciton
# image = radio_button_function()