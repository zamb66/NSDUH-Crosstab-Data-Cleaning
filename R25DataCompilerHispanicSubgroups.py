import pandas as pd
import numpy as np

def main():

	drug_names = ['Total','Alcohol', 'Cocaine', 'Hallucinogens', 'Heroin', 'Inhalants', 'Marijuana', 'PainReliever', 'Sedatives', 'Stimulants', 'Tranquilizer', 'Psychotheraputic']
	variable_types = ['phatcomplement', 'SEphatcomplement', 'low95cicomplement', 'high95cicomplement', 'WeightedCountsComplement', 'SEWeightedCountsComplement']
	total_types = ['phat', 'SEphat', 'low95ci', 'high95ci', 'WeightedCounts', 'SEWeightedCounts']
	age_columns = ['Mexican','Puerto Rican', "Central/South American","Cuban", 'Non-Hispanic']
	variable_labels = []
	subtracted_types = ['subtractedphat', 'subtractedweightedcounts']
	subtracted_labels = []

#Desired row and columns cells for total (in their location with header stripped)
	row_values = [5,6,7,8,9]
	col_values = [6,7,8,9,14,15]

	column_count = 0
	row_count = 0
	ROW_TOTALCOUNT = len(row_values)

#Subsequent for-loop creates final header names
	for x in drug_names:
		if x == 'Total':
			for a in total_types:
				variable_labels.append(x+a)
		else:
			for a in variable_types:
				variable_labels.append(x+a)

#Creates DataFrame with age_columns as row names and variable_labels as column names
	new_dataset = pd.DataFrame(index = age_columns, columns = variable_labels)

	total_dependence_data = pd.read_csv("TotalDrugDependenceHispanicSubgroups.csv")

#Runs through total csv file column by column, picking up desired cells as it progresses through rows
	for y in col_values:
		for x in row_values:
			new_dataset.at[age_columns[row_count], variable_labels[column_count]] = total_dependence_data.iloc[x,y]
			print("1")
			print(row_count)
			if ((row_count + 1) % ROW_TOTALCOUNT == 0):
				row_count = 0
				column_count +=1
			else:
				row_count +=1

	drug_names = drug_names[1:]
	print(drug_names)

#Different files require the the changing of which columns we go through
	col_values = [7,8,9,10,15,16]

#Same process as above, but we iterate through all of the files in this case
	for i in drug_names:
		temp_drug_file_name = "No" + i + "DependenceHispanicSubgroups.csv"
		temp_drug_dataset = pd.read_csv(temp_drug_file_name)
		for a in col_values:
			for b in row_values:
				new_dataset.at[age_columns[row_count], variable_labels[column_count]] = temp_drug_dataset.iloc[b,a]
				print("1")
				print(row_count)
				if ((row_count + 1) % ROW_TOTALCOUNT == 0):
					row_count = 0
					column_count +=1
				else:
					row_count +=1

#Sets up DataFrame headers for the subtracted values we will calculate
	for x in drug_names:
		for a in subtracted_types:
			subtracted_labels.append(x+a)


	subtracted_vals = pd.DataFrame(index = age_columns, columns = subtracted_labels)

	print(subtracted_vals)

#banana_row is a list that goes from 0, 1, to n-1, where n is the number of rows you have
	banana_row = [0,1,2,3,4]
	a = -1*len(subtracted_types)

#Performs subtracting and adds the value to the subtracted_vals DataFrame
	for i in drug_names:
		temp_variable_label = i + 'phatcomplement'
		weighted_count_temp_label = i + "WeightedCountsComplement"
		a += len(subtracted_types)
		for b in banana_row:
			subtracted_vals.at[age_columns[b], subtracted_labels[a]] = new_dataset.iloc[b, 0] - new_dataset.loc[age_columns[b], temp_variable_label]
			subtracted_vals.at[age_columns[b], subtracted_labels[a+1]] = new_dataset.iloc[b, 4] - new_dataset.loc[age_columns[b], weighted_count_temp_label]
			print(i)
				

	print(subtracted_vals)


	
#Combines our two DataFrames by joining columns next to one another
	new_dataset = pd.concat([new_dataset, subtracted_vals], axis = 1)
				

	new_dataset.to_csv('final_dataset.csv')


if __name__ == "__main__":
	main()
