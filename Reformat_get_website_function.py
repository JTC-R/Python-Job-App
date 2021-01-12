def inappropriate_answer(answer, possible_yes, possible_no, website):
    while answer not in possible_yes and answer not in possible_no:
        if(answer == 'answer_two'):
            print(f'Please answer Yes or No.')
            print(f'Do you want to search: {website}? (Yes/No) ')
        if(answer == 'answer_three'):
            print(f'Please answer Yes or No or \'Cancel\' to exit the program. ')
            print(f'Do you want ')


#Neeed to fix!
def get_websites():
    chosen_website = []
    possible_websites = make_website_list()
    possible_yes = make_yes_list()
    possible_no = make_no_list()
    answer_one = input(f"Do you want to search all websites?\n Websites are: {make_website_list()} ")
    if(answer_one in possible_yes):
        chosen_website = possible_websites
    elif(answer_one in possible_no):
        for website in possible_websites:
            answer_two = input(f'Do you want to search: {website}? (Yes/No) ')
            if(answer_two in possible_yes):
                chosen_website.append(website)
            elif(answer_two not in possible_yes and answer_two not in possible_no):

    elif(answer_one not in possible_yes and answer_one not in possible_no):
        while answer_two not in possible_yes and answer_two not in possible_no and answer_two != 'Cancel':
            print(f'Please indicate either Yes or No or type \'Cancel\' to exit program.' )
            answer_two = input(f"Do you want to search all websites?\n Websites are: {make_website_list()} ")
        if(answer_two == 'Cancel'):
            exit()



