import streamlit as st
import os, io

try: import wget
except: os.system('pip install wget'); import wget

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt


###################### Navigation on Sidebar ############################
Section = st.sidebar.selectbox('App Index',				
		('Dataset Overview', 			
		 'Explorative Analysis', 'Pre-Processing'))

if Section == 'Dataset Overview':
	OverviewOption = st.sidebar.selectbox('Overview Options',				
		('Dataset Summaries',
		 'NULLs Treatment')) 		 
		 
elif Section == 'Explorative Analysis':
	GraphOption = st.sidebar.selectbox('Options',				
		('Correlation Heatmap',
		 'Explore Individual features', 			
		 'Explore feature pairs', 
		 'Explore feature pairs split by a category'))
		 
###################### END Navigation Sidebar ###########################


################################# HELPER FUNCTIONS ########################################

def check_and_download_dataset(URL):
	dataset = wget.detect_filename(Dataset_URL)
	if not os.path.isfile(dataset): 
		os.system(f'wget -O {dataset} {Dataset_URL}')
		data_load_state = st.text(f'File {dataset} successfully downloaded from URL')
	else: 
		data_load_state = st.text(f'File already exists locally. Using local file.')
	return dataset, data_load_state

@st.cache  
def load_data(filename):
	def Detect_datetime(df):
		date_time_cols = []
		for i in df.select_dtypes(['object']).columns:
			try :
				_ = pd.to_datetime(df[i])
				date_time_cols.append(i)
			except ValueError: continue
		df[date_time_cols] = df[date_time_cols].apply(pd.to_datetime, axis=0)
		return df

	if '.xlsx' in dataset: 
		data_load_state.text('.xlsx file detected!')
		df = pd.read_excel(dataset)
	else: 
		try :
			data_load_state.text('.csv file detected!')  
			df = pd.read_csv(dataset, error_bad_lines=False)
			df.drop(columns='Unnamed: 0', inplace=True)    
		except UnicodeDecodeError:
			df = pd.read_csv(dataset, encoding = "ISO-8859-1", error_bad_lines=False)
			df.drop(columns='Unnamed: 0', inplace=True)
	data_load_state.text('Detecting datetime columns..')
	df = Detect_datetime(df)
	data_load_state.text('Succesfully Ingested and Loaded dataset!')
	return df
	
@st.cache
def treat_nulls(df_, treatment_numeric, treatment_string, treatment_datetime, drop_threshold=100):
	## Drop Columns
	percentage = df_.isnull().sum()/df_.isnull().count()*100
	drop_list = list(percentage[percentage > drop_threshold].index)
	df_.drop(columns = drop_list, inplace=True)
	## Datetime treatments
	if treatment_datetime == 'Replace Null with Max value':
		for i in df.select_dtypes(include='datetime64').columns: 
			df_[column].fillna(df_[column].max(), inplace=True)
	elif treatment_datetime == 'Replace Null with Min value':
		for i in df.select_dtypes(include='datetime64').columns: 
			df_[column].fillna(df_[column].min(), inplace=True)
	elif treatment_numeric == "Delete rows with Null":
		df_ = df_.merge(df_[df.select_dtypes(include='datetime64').columns].dropna(axis=0), 
					left_index=True, right_index=True, how='inner', suffixes=('', '_y'))
	## Numeric treatments
	summary_tab = df_.describe()
	if treatment_numeric == 'Replace Null with Mean':
		for column, value in summary_tab.loc['mean',:].items():
			df_[column].fillna(value, inplace=True)
	elif treatment_numeric == 'Replace Null with Max':
		for column, value in summary_tab.loc['max',:].items():
			df_[column].fillna(value, inplace=True)
	elif treatment_numeric == 'Replace Null with Min':
		for column, value in summary_tab.loc['min',:].items():
			df_[column].fillna(value, inplace=True)
	elif treatment_numeric == 'Replace Null with Zero':
		for column, value in summary_tab.loc['max',:].items():
			df_[column].fillna(0, inplace=True)
	elif treatment_numeric == "Fill-in Null with Moving Average":
		for column, value in summary_tab.loc['max',:].items():
			df_[column].fillna(df_[column].rolling(6).mean(), inplace=True)
	elif treatment_numeric == "Delete rows with Null":
		df_ = df_.merge(df_[list(summary_tab.columns)].dropna(axis=0), left_index=True, right_index=True, how='inner', suffixes=('', '_y'))
	## String treatments
	strings_Cols = list(df_.select_dtypes(include='object').columns)
	if treatment_string == 'Replace Null with most frequent':
		for column in strings_Cols:
			df_[column].fillna(df_[column].value_counts().iloc[0:1].index[0], inplace=True)
	elif treatment_string == 'Replace Null with empty string':
		for column in strings_Cols:
			df_[column].fillna('', inplace=True)
	elif treatment_string == "Delete rows with Null":
		df_ = df_.merge(df_[strings_Cols].dropna(axis=0), left_index=True, right_index=True, how='inner',suffixes=('', '_y'))
	df_.drop([x for x in df_ if x.endswith('_y')], axis=1, inplace=True)
	return df_

############################ END HELPER FUNCTIONS ################################

############################# BODY LAYOUTS #######################################
st.title('Test App: Data Preview')
st.header('Ingest & Load file')
Dataset_URL = st.text_input("URL to dataset (.csv or .xlsx format)")
try: df.shape
except:
	if Dataset_URL:
		dataset, data_load_state = check_and_download_dataset(Dataset_URL)
		df = load_data(dataset)	
if st.checkbox('Show Preview of dataset'):
	try: 		
		st.subheader('First 10 rows of dataset')
		st.write(df.head(10)) 
	except: st.text('No dataset detected!')	
st.write('------------')
	
try: 
	df

	if Section == 'Dataset Overview': 
		st.header('Dataset Overview')
	####################### Dataset Overview ################################
		if OverviewOption == "Dataset Summaries": #### Dataset Summaries
			buffer = io.StringIO()
			df.info(buf=buffer)
			s = buffer.getvalue()
			st.text(s)
			if st.checkbox('Show Numeric Summary'):		
				st.subheader('Summary of Numeric columns')
				st.write(df.describe().round(2))
			if st.checkbox('Show Datetime Summary'):		
				st.subheader('Summary of Datetime columns')
				if len(df.select_dtypes(include='datetime64').columns) == 0:
					st.write('No DateTime column detected')
				else:
					st.write(df.select_dtypes(include='datetime64').head())
			if st.checkbox('Show String Summary'):		
				st.subheader('Summary of String columns')
			try:
				df_type_objects = pd.concat([df.select_dtypes(include='object').nunique(),df.select_dtypes(include='object').apply(lambda x: list(pd.unique(x)),axis=0)],axis=1, join='inner')
				df_type_objects.rename(columns={0:'No. Unique values',1:'Unique Values'}, inplace=True)
				st.write(df_type_objects)
			except:
				st.write(pd.DataFrame(df.select_dtypes(include='object').nunique(),columns=['No. Unique Values']))
				st.write('\nErrors during analysis of string columns due to extreme number of unique values')
								###########################################
		elif OverviewOption == "NULLs Treatment": #### NULLs treatment
			st.header('Resolving issues with Null/NaN data')
			total_na_values = df.isnull().sum().sort_values(ascending=False)
			if total_na_values.sum() == 0: 
				st.text('No Null value detected! Yay!')
			else:
				st.subheader('Null Detected')
				try: st.table(empty)
				except:
					percentage = round(df.isnull().sum()/df.isnull().count()*100, 2).sort_values(ascending=False)
					empty = pd.concat([total_na_values[total_na_values>0], percentage[total_na_values>0]], axis=1, keys=['Null in Counts', 'Null in Percents'])
					st.table(empty)
			st.subheader('Drop column policy')
			Drop_Columns_Threshold = st.slider('Drop columns with more than X percent Nulls',  0, 99, 20)
			st.subheader('NULL treatment policies')
			Treatment_Choice_Numeric = st.selectbox("Treating Numeric Nulls", 
																							["Replace Null with Mean", 
																							 "Replace Null with Max", 
																							 "Replace Null with Min", 
																							 "Replace Null with Zero", 
																							 "Fill-in Null with Moving Average", 
																							 "Delete rows with Null"])
			Treatment_Choice_Datetime = st.selectbox("Treating Datetime Nulls", 
																							 ["Replace Null with Min", 
																								"Replace Null with Max", 
																								"Delete rows with Null"])  
			Treatment_Choice_String = st.selectbox("Treating String Nulls",
																						["Replace Null with most frequent", 
																						 "Replace Null with empty string", 
																						 "Delete rows with Null"])
			button_pressed = st.button('Apply Treatments!')
			if button_pressed:
				st.subheader('Null-treated result') 
				try: st.write(df_null_treated.isnull().sum())
				except:
					try: Drop_Columns_Threshold
					except: 
						Drop_Columns_Threshold = 100
					df_null_treated = treat_nulls(df.copy(), Treatment_Choice_Numeric, 
																									 Treatment_Choice_String,
																									 Treatment_Choice_Datetime, 
																									 Drop_Columns_Threshold)
					st.write(f'Total NULLs detected = {df_null_treated.isnull().sum().sum()}')
			
			Saved = st.button('Save changes to dataset!')
			if Saved:	df = 	df_null_treated									 
	######################## END Dataset Overview ###########################

	elif Section == 'Explorative Analysis': 
		st.header('Explorative Analysis')
		## create a {datatype: feature_names}
	####################### Explorative Analysis ################################
		
		if OverviewOption == "Correlation Heatmap": #### Correlation Heatmap
			## create UI that allows selection of multiple features (only numeric types)
			## create function that calculate the correlation of given features
			## Display sns.heatmap for correlation
			print()
								###########################################			
		elif OverviewOption == "Explore Individual features": #### Explore Individual features
			## create UI that allows selection of multiple features
			## seperate 2 groups: datetime & non-datetime
			## throw rejection warning against string features that have more than 20 unique values
			## create function that build a matplotlib grid corresponding to the size of non-datetime features set
			##                 that does distplot for numeric type & countplot for categorical types
			##                 that display the non-datetime plot
			## create function that build matplolib figures for datetime feature sets
			##                 that does countplot on various time level: years, months, weeks, days, hours, minutes
			print() 
								###########################################			
		elif OverviewOption == "Explore feature pairs": #### Explore feature pairs
			## create UI that allows selection of ONE key feature and multiple non-key features
			## create a graphing function that select the right graph type given the input features:
			##                   - cat x cat = violin x = keycat, y = count, hue = cat
			##                   - cat x numeric = bar plot
			##                   - numeric x numeric = scatter plot
			##                   - cat x datetime = count plot x = datetime, y = count, hue = cat
			##                   - nnumeric x datetime = lineplot
			##                   - datetime x datetime = error
			print()
								###########################################			
		elif OverviewOption == "Explore feature pairs split by a category": #### Explore feature pairs split by a category
			## create UI that allows selection of ONE key feature, ONE hue=cat and multiple non-key features
			## create a graphing function that select the right graph type given the input features:
			##                   key = datetime, hue = cat, only graph numeric inputs
			##                   key = numeric, hue = cat, input cat = violin plot y=sum(numeric)
			##                   key = numeric, hue = cat, input numeric = scatterplot 
			##                   key = numeric, hue = cat, input datetime = lineplot
			print()
									
	print('')								
	######################## END Explorative Analysis ###########################


except: 
	st.text('No dataset detected!! Please ingest dataset before continue')
########################### END BODY LAYOUT ############################
