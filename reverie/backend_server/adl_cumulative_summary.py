import pandas as pd
import re
# Define the classification list as a dictionary
classification_dict = {
    "Waking up and completing morning routine": "Personal care activities",
    "making coffee": "Household activities",
    "preparing breakfast": "Household activities",
    "eating breakfast": "Eating and drinking",
    "getting dressed": "Personal care activities",
    "unlocking the doors to Hobbs Cafe": "Working and work-related",
    "turning on the lights in the cafe": "Working and work-related",
    "turning on the furnace": "Working and work-related",
    "turning on the TV": "Working and work-related",
    "checking the inventory and restocking any items that are low": "Working and work-related",
    "setting up the counter and making sure everything is clean and organized": "Working and work-related",
    "preparing the coffee machine and other equipment for the day": "Working and work-related",
    "checking the schedule for the day and making sure all employees are aware of their shifts": "Working and work-related",
    "greeting customers as they enter the cafe": "Working and work-related",
    "taking orders and preparing drinks": "Working and work-related",
    "chatting with customers and making them feel welcome": "Working and work-related",
    "restocking supplies and cleaning the counter area": "Working and work-related",
    "taking a break to eat lunch": "Eating and drinking",
    "checking inventory and making a list of items to restock": "Working and work-related",
    "interacting with customers and taking orders": "Working and work-related",
    "preparing drinks and food orders": "Working and work-related",
    "cleaning and restocking the counter area": "Working and work-related",
    "taking a final break before closing the cafe": "Leisure and sports",
    "closing the cafe for her lunch break": "Eating and drinking",
    "turning off the furnace": "Working and work-related",
    "checking the inventory for the cafe": "Working and work-related",
    "making a list of items that need to be restocked": "Working and work-related",
    "placing an order for the items that need to be restocked": "Working and work-related",
    "restocking supplies and cleaning the counter": "Working and work-related",
   # "taking a break to eat lunch and check inventory": "Eating and drinking",
    "returning to the counter and continuing to interact with customers": "Working and work-related",
    "turning off the TV in the cafe": "Working and work-related",
    "wiping down the counter and tables": "Working and work-related",
    "washing and putting away dishes": "Working and work-related",
    "sweeping and mopping the floors": "Working and work-related",
    "taking out the trash": "Working and work-related",
    "preparing ingredients for dinner": "Household activities",
    "cooking dinner": "Household activities",
    "setting the table": "Household activities",
    "enjoying her dinner": "Eating and drinking",
    "cleaning up after dinner": "Household activities",
    "changing into comfortable clothes": "Personal care activities",
    "choosing a show or movie to watch": "Leisure and sports",
    "getting a snack or drink": "Eating and drinking",
    "watching the show or movie": "Leisure and sports",
    "closing the cafe and locking the doors": "Working and work-related",
    "counting the cash register and recording the day's sales": "Working and work-related",
    "cleaning and restocking the cafe for the next day": "Working and work-related",
    "washing her face and brushing her teeth": "Personal care activities",
    "setting her alarm for the next day": "Personal care activities",
    "going to bed and turning off the TV before falling asleep": "Personal care activities",
    "sleeping": "Personal care activities",
    "waking up and completing her morning routine": "Personal care activities",
    "waking up and getting out of bed" : "Personal care activities",
    "taking a shower and getting dressed" : "Personal care activities",
    "making breakfast" : "Household activities",
    "unlocking the cafe door" : "Working and work-related",

    "brewing a fresh pot of coffee" : "Household activities",
    "wiping down the tables and chairs" : "Working and work-related",
    "taking a quick break to drink her own cup of coffee" : "Eating and drinking",
    "enjoying her lunch" : "Eating and drinking",
    "greeting customers and taking their orders" : "Working and work-related",
    "making coffee and other drinks" : "Work and work-related",
    "serving food and drinks to customers" : "Work and work-related",
    "setting out fresh pastries and snacks" : "Work and work-related",
    "clearing tables and cleaning up after customers" : "Work and work-related",
    "restocking supplies and ingredients" : "Work and work-related",
    "taking a short break" : "Leisure and sports",
    "checking inventory and making a shopping list" : "Work and work-related",
    "preparing for the next day's menu" : "Household activities",
    "washing her hands" : "Personal care activities",
    "reflecting on her day ahead" :  "Personal care activities",
    "making a mental to-do list" : "Personal care activities",
    "closing her eyes and taking deep breaths" : "Personal care activities",
    "checking her progress" : "Personal care activities",
    "going to bed and falling asleep at 8:30 pm" : "Personal care activities",
    "completing her morning routine" : "Personal care activities",
    "preparing her lunch" : "Household activities",
    "setting up a table for herself":"Household activities",
    "sitting down to eat her lunch" :"Household activities",
    "cleaning up after her lunch" : "Household activities",
    "making herself a cup of tea" : "Household activities",
    "setting the table for dinner" : "Household activities",
    "cleaning up after breakfast" : "Household activities",
    "turning on the furnace and TV" : "Household activities",
    "setting up the pastries and snacks for display" : "Work and work-related",
    "preparing her bag with necessary items for the day"  : "Work and work-related",
    "checking inventory and restocking supplies" : "Work and work-related",
    "taking orders from customers" : "Work and work-related",
    "cleaning and organizing the counter area" :"Work and work-related",
    "watching TV":"Leisure and sports",
    "watching a cooking show" : "Leisure and sports",
    "walking back to her apartment" :"Leisure and sports",
    "taking a short break to walk around the cafe and greet customers":"Leisure and sports",
}

regex_to_category = {
    r"turning off.*": "Working and work-related",  # General "turning off" activities
    r"checking.*inventory.*": "Working and work-related",  # Inventory checks
    r"setting.*counter.*": "Working and work-related",  # Setting up counters
    r"restocking.*": "Working and work-related",  # Restocking supplies or items
    r"cleaning.*counter.*": "Working and work-related",  # Cleaning counters

    r"wiping.*(tables|chairs|counter).*": "Household activities",  # Wiping tables, chairs, or counters
    r"sweeping.*": "Household activities",  # Sweeping tasks
    r"taking.*break.*": "Leisure and sports",  # Any breaks
    r"greeting.*": "Working and work-related",  # Greeting activities
    r".*serving.*": "Working and work-related",  # Serving food or drinks
    r"reading.*": "Leisure and sports",  # Reading activities
    r"getting into bed.*": "Personal care activities",  # Bedtime routines
    r"washing.*(hands|dishes|face).*": "Personal care activities",  # Washing-related tasks
    r"setting.*alarm.*": "Personal care activities",  # Alarm-setting tasks
    r".*pajamas.*": "Personal care activities",  # Pajama-related activities
    r"making.*coffee": "Household activities",  # Making coffee
    r"preparing.*lunch": "Household activities",  # Preparing lunch
    r".*restocking supplies.*": "Working and work-related",  # Restocking supplies
    r".*customers.*": "Working and work-related",  # Customer interactions
    r".*cash register.*": "Working and work-related",  # Cash register-related tasks
    r".*cleaning tables.*": "Working and work-related",  # Cleaning tables
    r".*leftover.*(food|drinks).*": "Working and work-related",  # Handling leftovers
    r"(cleaning|organizing).*(tables|chairs).*": "Working and work-related",  # Cleaning/organizing tables or chairs
    r"brewing.*coffee": "Household activities",  # Brewing coffee
    r"drinking.*coffee": "Eating and drinking",  # Drinking coffee
    r"making.*coffee.*drinks": "Working and work-related",  # Making coffee drinks
    r"serving.*food.*drinks": "Working and work-related",  # Serving food and drinks
    r"clearing.*tables.*customers": "Working and work-related",  # Clearing tables after customers
    r"restocking.*ingredients": "Working and work-related",  # Restocking ingredients
    r"preparing.*next day's menu": "Household activities",  # Preparing menu for the next day
    r"setting up.*table.*": "Household activities",  # Setting up tables
    r"sitting down.*lunch": "Household activities",  # Sitting down for lunch
    r"cleaning up.*lunch": "Household activities",  # Cleaning up after lunch
    r"taking orders.*customers": "Working and work-related",  # Taking customer orders
    r"(cleaning|organizing).*(cafe|counter area)": "Working and work-related",  # Cleaning or organizing cafe/counter area
    r"walking.*cafe.*greet.*customers": "Leisure and sports",  # Walking around the cafe and greeting customers
    r"checking.*shopping list": "Working and work-related",  # Checking shopping list
    r"stretching.*light exercises": "Leisure and sports",  # Light exercises
    r"checking.*TV.*changing.*channel.*": "Leisure and sports",  # Changing TV channels
    r"checking.*(temperature|thermostat).*": "Personal care activities",  # Checking temperature/thermostat
    r"checking.*furnace.*turning.*off.*": "Personal care activities",  # Checking the furnace
    r"sitting down.*table.*turning on.*TV.*": "Leisure and sports",  # Sitting and watching TV
    r".*\b(phone|email|mail)\b.*": "Telephone calls, mail, and e-mail",  # Any phone, email, or mail activities
    r".*\b(unlocking|locking|cafe)\b.*": "Working and work-related",  # Any phone, email, or mail activities
    r"checking.*(temperature|thermostat).*": "Personal care activities",  # Matches any activity involving checking temperature or thermostat
    r"preparing.*coffee machine.*clean.*ready.*": "Working and work-related",  # Matches "Preparing the coffee machine and making sure it is clean and ready for use"
    r"heating.*lunch.*microwave.*": "Household activities",  # Matches "Heating up her lunch in the microwave"
    r"eating.*lunch.*": "Eating and drinking",  # Matches "Eating her lunch"
    r"taking.*payments.*giving.*change.*": "Working and work-related",  # Matches "Taking payments and giving change"
    r"checking.*responding.*emails.*messages.*": "Telephone calls, mail, and e-mail",  # Matches "Checking and responding to emails and messages"
    r"checking.*TV.*make sure.*turned off.*": "Household activities",  # Matches "Checking the TV to make sure it is turned off"
    r"checking.*TV.*turning.*off.*": "Household activities",  # Matches "Checking the TV and turning it off if it's still on"
    r".*\bknitting\b.*": "Leisure and sports",  # Matches any activity with "knitting"
    r".*\b(book|read|knit)\b.*": "Leisure and sports",  # Matches activities with "book" or "read"
    r".*\b(eating|drinking|sipping|drink|ear|sip)\b.*": "Eating and drinking",  # Matches activities with "eating", "drinking", "sipping", etc.
    r".*\b(comfortable|relax|wander|volume|news|watch|music|movie|deep breaths|favorite)\b.*": "Leisure and sports",  # Matches activities with "comfortable", "relax", or "wander"
    r".*\b(medication|teeth|dressing|dress|stretching)\b.*": "Personal care activities",  # Matches activities with "medication" or "teeth"
    r".*\b(selecting a channel to watch|putting on her favorite music|turning on the TV and adjusting the volume|taking a break and closing her eyes)\b.*":
    "Leisure and sports", 
    r".*\b(cash|camera|security|schedule)\b.*": "Working and work-related",  # Matches activities with "comfortable", "relax", or "wander"
    
    r".*\b(heating|pouring|sitting|wiping|leftovers|tea)\b.*": "Household activities",  # Matches activities with "comfortable", "relax", or "wander"
    
}



default_category = "Other activities"

# Categorization function using exact match
def categorize_activity(activity):
    # First, try exact match
    if activity in classification_dict:
        return classification_dict[activity]
    
    # If no exact match, try regex matching
    for pattern, category in regex_to_category.items():
        if re.search(pattern, activity, re.IGNORECASE):  # Case-insensitive matching
            return category
    
    # Default to "Other activities" if no match
    return default_category


# Example usage with DataFram1
# Define the base file name
base_name = "final_maria_3"  # Replace this with your desired base name

# File paths
input_file = f"activity_summary_{base_name}.csv"  # Input CSV file
categorized_output_file = f"adl_activity_summary_{base_name}.csv"  # Categorized output file
category_totals_output_file = f"category_totals_{base_name}.csv"  # Totals output file

# Load the input CSV file
df = pd.read_csv(input_file)

# Add category column using a function (assumes categorize_activity is defined)
df['Category'] = df['Activity'].apply(categorize_activity)

# Save categorized results to a CSV
df.to_csv(categorized_output_file, index=False)

# Load the categorized file
df = pd.read_csv(categorized_output_file)

# Group by category and calculate the total time in minutes
category_totals = df.groupby("Category")["Total Time (seconds)"].sum().reset_index()
category_totals["Total Time (minutes, sum)"] = category_totals["Total Time (seconds)"] / 60

# Rename columns for clarity and drop the original seconds column (optional)
category_totals.drop(columns=["Total Time (seconds)"], inplace=True)

# Save the totals to a new CSV file
category_totals.to_csv(category_totals_output_file, index=False)

print(f"Categorized results saved to '{categorized_output_file}'.")
print(f"Total time for each category has been calculated and saved to '{category_totals_output_file}'.")
