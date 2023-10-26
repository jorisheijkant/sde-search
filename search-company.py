# Search for a company in the database, and output a csv file of all subsidies found, with a total
import xml.etree.ElementTree as ET
import sys
import csv

# Load the xml file
tree = ET.parse('data/sde.xml')

# Get the root element
root = tree.getroot()

# List the amount of subsidies
print("Number of subsidies: ", len(root))

# Get the argument from the command line
company = sys.argv[1]

# List the properties to search for the company name
properties = ['Titel', 'Berichttekst', 'Projectpartner-s-', 'Aanvrager-ontvanger']

# Create a list of all subsidies that match the company name
subsidies = []

# Loop through all subsidies
for subsidy in root:
    # Loop through all properties
    for property in properties:
        if(subsidy.find(property) == None or subsidy.find(property).text == None):
            continue
        # Check if the company name is in the property, both capitalized and not capitalized
        if(company in subsidy.find(property).text or company.capitalize() in subsidy.find(property).text):
            # Add the subsidy to the list if it is not already in there
            if(subsidy not in subsidies):
                subsidies.append(subsidy)

# Print the amount of subsidies found
print("Number of subsidies found: ", len(subsidies))

# Convert the subsidies to a csv file
with open(f"data/output/{company}.csv", 'w', newline='') as csvfile:
    # Create a csv writer
    subsidywriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    total = 0
    
    # Loop through all subsidies
    for subsidy in subsidies:
        # Get the title
        title = subsidy.find('Titel').text
        
        # Get the amount, strip it of euro sign, spaces and dots and all non-numeric characters
        amount_string = subsidy.find('Budget').text
        amount = [char for char in amount_string if char.isdigit() or char == ',']
        amount = ''.join(amount)
        amount = amount.replace(',', '.')
        
        if(amount == ''):
            continue
        amount = float(amount)
        # Round to integers
        amount = round(amount)
        
        # Get the applicant
        applicant = subsidy.find('Aanvrager-ontvanger').text

        # Get the year
        year = subsidy.find('Jaar').text
        year = year.replace(' ', '')

        # Get the project partners
        partners = subsidy.find('Projectpartner-s-').text
       
        # Get the description
        description = subsidy.find('Berichttekst').text

        print(f"{title} - {amount}")

        # Add the amount to the total
        total += int(amount)
            
        # Write the row
        subsidywriter.writerow([title, amount, applicant, year, partners, description])

# Sort rows by year, descending
with open(f"data/output/{company}.csv", 'r', newline='') as csvfile:
    # Create a csv reader
    subsidyreader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # Sort the rows by year, descending
    sortedlist = sorted(subsidyreader, key=lambda row: row[3], reverse=True)

# Write the sorted rows to the csv
with open(f"data/output/{company}.csv", 'w', newline='') as csvfile:
    # Create a csv writer
    subsidywriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # Write the header
    subsidywriter.writerow(['Titel', 'Bedrag', 'Aanvrager', 'Jaar', 'Partners', 'Omschrijving'])
    # Write the sorted rows
    subsidywriter.writerows(sortedlist)

# Print the total amount of subsidies
print("Total amount of subsidies: ", total)

# Write the total of subsidies to the csv
with open(f"data/output/{company}.csv", 'a', newline='') as csvfile:
    # Create a csv writer
    subsidywriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # Write the total
    subsidywriter.writerow(['Total', total, '', '', ''])