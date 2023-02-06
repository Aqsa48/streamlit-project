import streamlit as st
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import warnings
import time
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go



st.set_page_config(
    page_title="Fraud Detection Case Study",
    page_icon="👋",
)

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
pd.set_option('display.max_columns', 300) #Setting column display limit
plt.style.use('ggplot') #Applying style to graphs




@st.cache
def load_csv():
        csv=pd.read_csv("application_data.csv")
        return csv
df=pd.read_csv("application_data.csv")
df2=pd.DataFrame()

with st.spinner('Wait for it...'):
    time.sleep(5)
    
   


tab1, tab2, tab3,tab4 = st.tabs(["Overview ", "Data Wrangling", "EDA","Model Prediction"])

with tab1:
   
    st.header("**Exploratory Data Analysis (EDA) – Credit Card Fraud Detection Case Study**")
    st.subheader("Overview")
    
    st.markdown('''In this case study, the focus is on Exploratory Data Analysis for credit card fraud detection.
            The goal is to gain insights from the data to help detect fraudulent activities and ultimately improve business growth.
            Through data analysis, we aim to uncover patterns and relationships within the data that can be used to identify fraudulent behavior.
            The end result of this case study will provide a better understanding of the credit card fraud landscape and offer practical strategies for detecting and preventing fraud''')
    
    st.subheader("**Business Problem**")
    st.markdown('''The problem of loan default by customers is a major concern for companies and banks as it results in significant financial losses. In order to mitigate this problem, companies are turning towards Exploratory Data Analysis (EDA) to detect potential loan defaults and prevent financial losses. The objective of this study is to use EDA techniques to understand the patterns and relationships in loan data to detect potential loan defaults and help companies grow their business.''')
    
    st.subheader("**Business Goal**")
    st.markdown('''The business goal of this case study is to determine the creditworthiness of loan applicants, specifically to assess the likelihood of their ability to repay the loan installment. The aim is to minimize loan default rates and improve the financial performance of the company or bank by providing loans only to those customers who have the capacity to repay it.''')
    

with tab2:
  
   
   st.header("Import DataSet")
   st.write(df.head())
   rows,col=df.shape
   
   st.write(f"DataFrame contains Rows : {rows} and Columns : {col}",)
   info=df.info()
   st.text("")
   st.text("Summery Statistic ")
   st.write(df.describe())
   
   st.text("")
   st.text("")
   col1, col2, = st.columns(2)

   with col1:
      st.subheader("Missing values in Percentage %")
      st.write((df.isnull().sum()/len(df)*100).sort_values(ascending=False).head(20))
   

   with col2:
      st.write("")
      st.write("")
      st.write("")
      st.subheader("Insight")
      st.markdown("These observations suggest that the data is messy and requires preprocessing before conducting further analysis. The high percentage of missing values can impact the accuracy of the analysis, while the presence of negative values and outliers can skew the results. Cleaning and preprocessing the data is crucial to ensure that the findings are accurate and meaningful.")
   
   
   st.subheader("Handling Missing Data")
   
   st.write("We set 35 percent as a treshold ,drop all columns that have greater then 35 percent ")
   with st.echo():
     
      missing_col=(df.isnull().sum()).sort_values(ascending=False)
      missing_col=missing_col[missing_col.values >0.35*len(df)]
   
   st.write('')
   st.write("These are all columns that have greater then 35 percent")
   fig = plt.figure(figsize=(25, 4))
   sns.barplot(x=missing_col.index,y=missing_col.values)
   plt.xticks(rotation=60,)   
   st.pyplot(fig)
   
   st.write("")
   st.subheader("Observations")   
   st.write("We discovered that 49 columns have more than 35% of missing values, so we decided to remove those columns from our data.")

   missing_label=missing_col.index
   df.drop(columns=missing_label,axis=1,inplace=True)
   st.write("shape of the new data frame is")

   st.write(df.shape)
   
   st.write("")
   st.write("After removing null values, check the percentage of null values for each column again")
   st.write("")
   st.write((df.isnull().sum()/len(df)*100).sort_values(ascending=False).head(20))
   
   st.write("")
   st.write("")
   st.write("Impute the cetagorical missing values by mode using simple imputer")

   with st.echo():
      # explicitly require this experimental feature
      from sklearn.experimental import enable_iterative_imputer  # noqa
      # now you can import normally from sklearn.impute
      from sklearn.impute import SimpleImputer

      imp = SimpleImputer(missing_values=np.nan,strategy='most_frequent')

      col_name=['AMT_REQ_CREDIT_BUREAU_YEAR',
       'AMT_REQ_CREDIT_BUREAU_QRT', 'AMT_REQ_CREDIT_BUREAU_MON',
       'AMT_REQ_CREDIT_BUREAU_WEEK', 'AMT_REQ_CREDIT_BUREAU_DAY',
       'AMT_REQ_CREDIT_BUREAU_HOUR', 'NAME_TYPE_SUITE',
       'OBS_30_CNT_SOCIAL_CIRCLE', 'DEF_30_CNT_SOCIAL_CIRCLE',
       'OBS_60_CNT_SOCIAL_CIRCLE', 'DEF_60_CNT_SOCIAL_CIRCLE',
       'AMT_GOODS_PRICE', 'AMT_ANNUITY', 'CNT_FAM_MEMBERS',
       'DAYS_LAST_PHONE_CHANGE']
      df[col_name]=imp.fit_transform(df[col_name])

   st.write("")
   st.write("")
   st.write("Impute the numerical missing values by median using simple imputer")

   with st.echo():
      imp = SimpleImputer(missing_values=np.nan,strategy='median')

      col_name=["EXT_SOURCE_3","EXT_SOURCE_2"]
      df[col_name]=imp.fit_transform(df[col_name])

   st.write("")
   st.write("")
   st.markdown("If you observe the columns carefully, you will find that Days columns contain an Negative values. So let’s make some changes")

   with st.echo():
      abs_col=['DAYS_BIRTH', 'DAYS_EMPLOYED', 'DAYS_REGISTRATION', 'DAYS_ID_PUBLISH',
       'DAYS_LAST_PHONE_CHANGE']
      df[abs_col]=df[abs_col].abs()
   
   
   
   st.markdown("""Some cetagorical feature have XNA values . In "CODE_GENDER" we impute with F.also we observed that  columns "ORGANIZATION_TYPE" in which missing values are missing at ramdom.it depands on NAME_INCOME_TYPE with pensionar""")   
    
   col1, col2, = st.columns(2)  
   with col1:
      st.write(df[['ORGANIZATION_TYPE','NAME_INCOME_TYPE']].head(30)) 
   

   with col2:
      st.write("")
      st.write("")
      st.write("")
      
      with st.echo():
         df.loc[df["CODE_GENDER"]=="XNA","CODE_GENDER"]="F"
         df.loc[df["ORGANIZATION_TYPE"]=="XNA","ORGANIZATION_TYPE"]="Pensioner"
         df.loc[df["NAME_FAMILY_STATUS"]=="Unknown","NAME_FAMILY_STATUS"]="Married"
         df['OCCUPATION_TYPE'].fillna('Pensioner' , inplace = True)
      
      
      st.markdown("Binning the birth days into age  group")
      with st.echo():
         df["DAYS_BIRTH"]=(df['DAYS_BIRTH']/360).astype("int")
         df["AGE_GROUP"]=pd.cut(df["DAYS_BIRTH"],bins=[19,25,35,60,100],labels=['Very_Young','Young', 'Middle_Age', 'Senior_Citizen'])
      
      
   st.write("")
   st.write("")
   st.subheader("Type Casting")
   st.write("we observed that some need to type cast into category")
   with st.echo():
      df["TARGET"]=df["TARGET"].astype("category")
      df["NAME_CONTRACT_TYPE"]=df["NAME_CONTRACT_TYPE"].astype("category")
      df["CODE_GENDER"]=df["CODE_GENDER"].astype("category")
      df["FLAG_OWN_CAR"]=np.where(df["FLAG_OWN_CAR"]=="y",1,0)
      df["FLAG_OWN_REALTY"]=np.where(df["FLAG_OWN_REALTY"]=="y",1,0)
      df["AMT_ANNUITY"]=df["AMT_ANNUITY"].astype("float")
      df["AMT_GOODS_PRICE"]=df["AMT_GOODS_PRICE"].astype("float")
      df["NAME_TYPE_SUITE"]=df["NAME_TYPE_SUITE"].astype("category")
      df["NAME_INCOME_TYPE"]=df["NAME_INCOME_TYPE"].astype("category")
      df["NAME_EDUCATION_TYPE"]=df["NAME_EDUCATION_TYPE"].astype("category")
      df["NAME_FAMILY_STATUS"]=df["NAME_FAMILY_STATUS"].astype("category")
      df["NAME_HOUSING_TYPE"]=df["NAME_HOUSING_TYPE"].astype("category")
      df["OCCUPATION_TYPE"]=df["OCCUPATION_TYPE"].astype("category")
      df["CNT_FAM_MEMBERS"]=df["CNT_FAM_MEMBERS"].astype("category")
      df["ORGANIZATION_TYPE"]=df["ORGANIZATION_TYPE"].astype("category")
      df["WEEKDAY_APPR_PROCESS_START"]=df["WEEKDAY_APPR_PROCESS_START"].astype("category")
      df["DAYS_LAST_PHONE_CHANGE"]=df["DAYS_LAST_PHONE_CHANGE"].astype("float")
   
   
   st.subheader("Feature Selection")   
   st.write("Check The Variance Thresholds of each coloumns")
   ### It will zero variance features
   numerical_col=df.select_dtypes(include="number")
   from sklearn.feature_selection import VarianceThreshold
   with st.echo():
      
      var_thres=VarianceThreshold(threshold=0)
      var_thres.fit(numerical_col)
      constant_columns = [column for column in numerical_col.columns
                    if column not in numerical_col.columns[var_thres.get_support()]]

   st.write("Total number of columns that dont have variance ",len(constant_columns))
   st.write(constant_columns)
   
   X=numerical_col
   y=df["TARGET"]
   from sklearn.model_selection import train_test_split
   X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=0)
   
   # with the following function we can select highly correlated features
# it will remove the first feature that is correlated with anything other feature
   with st.echo():
      def correlation(dataset, threshold):
         col_corr = set()  # Set of all the names of correlated columns
         corr_matrix = dataset.corr()
         for i in range(len(corr_matrix.columns)):
            for j in range(i):
                  if abs(corr_matrix.iloc[i, j]) > threshold: # we are interested in absolute coeff value
                     colname = corr_matrix.columns[i]  # getting the name of column
                     col_corr.add(colname)
         return col_corr
   
      corr_features = correlation(X_train, 0.8)
   st.write("Get those columns that higly correlated each other",len(set(corr_features)))
   st.write(corr_features)
      

   fig = plt.figure(figsize=(15, 4))
   sns.countplot(x='TARGET',hue='FLAG_DOCUMENT_7',data=df, palette = 'Set2')
   plt.title("Gender Distribution in Target")  
   st.pyplot(fig) 
   
   num_corr=df[['FLAG_DOCUMENT_2', 'FLAG_DOCUMENT_3',
       'FLAG_DOCUMENT_4', 'FLAG_DOCUMENT_5', 'FLAG_DOCUMENT_6',
       'FLAG_DOCUMENT_7', 'FLAG_DOCUMENT_8', 'FLAG_DOCUMENT_9',
       'FLAG_DOCUMENT_10', 'FLAG_DOCUMENT_11', 'FLAG_DOCUMENT_12',
       'FLAG_DOCUMENT_13', 'FLAG_DOCUMENT_14', 'FLAG_DOCUMENT_15',
       'FLAG_DOCUMENT_16', 'FLAG_DOCUMENT_17', 'FLAG_DOCUMENT_18',
       'FLAG_DOCUMENT_19', 'FLAG_DOCUMENT_20', 'FLAG_DOCUMENT_21']]
   
   num_corr1=df[['SK_ID_CURR', 'CNT_CHILDREN',
       'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY', 'AMT_GOODS_PRICE',
       'REGION_POPULATION_RELATIVE', 'DAYS_BIRTH', 'DAYS_EMPLOYED',
       'DAYS_REGISTRATION', 'DAYS_ID_PUBLISH', 'FLAG_MOBIL', 'FLAG_EMP_PHONE',
       'FLAG_WORK_PHONE', 'FLAG_CONT_MOBILE', 'FLAG_PHONE', 'FLAG_EMAIL',
       'REGION_RATING_CLIENT', 'REGION_RATING_CLIENT_W_CITY',
       'HOUR_APPR_PROCESS_START', 'REG_REGION_NOT_LIVE_REGION',
       'REG_REGION_NOT_WORK_REGION', 'LIVE_REGION_NOT_WORK_REGION',
       'REG_CITY_NOT_LIVE_CITY', 'REG_CITY_NOT_WORK_CITY',
       'LIVE_CITY_NOT_WORK_CITY', 'EXT_SOURCE_2', 'EXT_SOURCE_3',
       'DAYS_LAST_PHONE_CHANGE',]]   


   st.write("")
   st.write("Correlation between all the columns that name FLAG_DOCUMENT")   
   fig1 =plt.figure(figsize=(25,25))
   sns.heatmap(num_corr.corr(),annot=True)
   st.pyplot(fig1)   

   st.write("")
   st.markdown("we observed that these are all columns are not related in our case study.so we drop all those columns")   

   with st.echo():
      unwanted=['FLAG_OWN_CAR', 'FLAG_OWN_REALTY','FLAG_MOBIL', 'FLAG_EMP_PHONE', 'FLAG_WORK_PHONE', 'FLAG_CONT_MOBILE',
       'FLAG_PHONE', 'FLAG_EMAIL','REGION_RATING_CLIENT','REGION_RATING_CLIENT_W_CITY','FLAG_EMAIL', 'REGION_RATING_CLIENT',
       'REGION_RATING_CLIENT_W_CITY', 'FLAG_DOCUMENT_2', 'FLAG_DOCUMENT_3','FLAG_DOCUMENT_4', 'FLAG_DOCUMENT_5', 'FLAG_DOCUMENT_6',
       'FLAG_DOCUMENT_7', 'FLAG_DOCUMENT_8', 'FLAG_DOCUMENT_9','FLAG_DOCUMENT_10', 'FLAG_DOCUMENT_11', 'FLAG_DOCUMENT_12',
       'FLAG_DOCUMENT_13', 'FLAG_DOCUMENT_14', 'FLAG_DOCUMENT_15','FLAG_DOCUMENT_16', 'FLAG_DOCUMENT_17', 'FLAG_DOCUMENT_18',
       'FLAG_DOCUMENT_19', 'FLAG_DOCUMENT_20', 'FLAG_DOCUMENT_21']  

   unwanted=['AMT_GOODS_PRICE','LIVE_CITY_NOT_WORK_CITY','LIVE_REGION_NOT_WORK_REGION','FLAG_OWN_CAR', 'FLAG_OWN_REALTY','FLAG_MOBIL', 'FLAG_EMP_PHONE', 'FLAG_WORK_PHONE', 'FLAG_CONT_MOBILE',
       'FLAG_PHONE', 'FLAG_EMAIL','REGION_RATING_CLIENT','REGION_RATING_CLIENT_W_CITY','FLAG_EMAIL', 'REGION_RATING_CLIENT',
       'REGION_RATING_CLIENT_W_CITY', 'FLAG_DOCUMENT_2', 'FLAG_DOCUMENT_3','FLAG_DOCUMENT_4', 'FLAG_DOCUMENT_5', 'FLAG_DOCUMENT_6',
       'FLAG_DOCUMENT_7', 'FLAG_DOCUMENT_8', 'FLAG_DOCUMENT_9','FLAG_DOCUMENT_10', 'FLAG_DOCUMENT_11', 'FLAG_DOCUMENT_12',
       'FLAG_DOCUMENT_13', 'FLAG_DOCUMENT_14', 'FLAG_DOCUMENT_15','FLAG_DOCUMENT_16', 'FLAG_DOCUMENT_17', 'FLAG_DOCUMENT_18',
       'FLAG_DOCUMENT_19', 'FLAG_DOCUMENT_20', 'FLAG_DOCUMENT_21']

   
   df.drop(columns=unwanted,axis=1,inplace=True)
   df2=df.copy()
   st.write(df.head())
   
   
   numerical = ['CNT_CHILDREN', 'AMT_INCOME_TOTAL', 'AMT_CREDIT',
       'AMT_ANNUITY', 'REGION_POPULATION_RELATIVE',
       'DAYS_BIRTH','DAYS_EMPLOYED', 'DAYS_REGISTRATION', 'DAYS_ID_PUBLISH',
       'HOUR_APPR_PROCESS_START','EXT_SOURCE_2', 'EXT_SOURCE_3',
       'DAYS_LAST_PHONE_CHANGE' ]
   # Create a figure and axis
   
   st.subheader("Check Outliers")
   

   fig4, axes = plt.subplots(nrows=3, ncols=5, figsize=(20, 20), sharey=True,)

   # Flatten the axes array
   axes = axes.flatten()

   # Plot the box plots
   for ax, col in zip(axes, numerical):
      sns.boxplot(x=df[col], ax=ax,color="green")
      ax.set_title(col)

      # Show the plot
   st.pyplot(fig4)



   st.write("")
   st.write("")
   st.subheader("Removing Outliers")
   st.write("")
   # Define a function to remove outliers using IQR
   with st.echo():
      def remove_outliers(df, columns):
         for col in columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df = df[(df[col] > lower_bound) & (df[col] < upper_bound)]
         return df

   # Apply the function to the desired columns
   data1 = remove_outliers(df, numerical)
   
   st.write("")
   fig4, axes = plt.subplots(nrows=3, ncols=5, figsize=(20, 20), sharey=True,)

   # Flatten the axes array
   axes = axes.flatten()

   # Plot the box plots
   for ax, col in zip(axes, numerical):
      sns.boxplot(x=data1[col], ax=ax,color="green")
      ax.set_title(col)

      # Show the plot
   st.pyplot(fig4)

   x=[ 'TARGET', 'NAME_CONTRACT_TYPE', 'CODE_GENDER',
       'NAME_TYPE_SUITE', 'NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE',
       'NAME_FAMILY_STATUS', 'NAME_HOUSING_TYPE', 
       'OCCUPATION_TYPE', 'WEEKDAY_APPR_PROCESS_START',
        'REG_REGION_NOT_LIVE_REGION',
       'REG_REGION_NOT_WORK_REGION', 'REG_CITY_NOT_LIVE_CITY',
       'REG_CITY_NOT_WORK_CITY', 'ORGANIZATION_TYPE',  'AMT_REQ_CREDIT_BUREAU_HOUR',
       'AMT_REQ_CREDIT_BUREAU_DAY', 'AMT_REQ_CREDIT_BUREAU_WEEK',
       'AMT_REQ_CREDIT_BUREAU_MON', 'AMT_REQ_CREDIT_BUREAU_QRT',
       'AMT_REQ_CREDIT_BUREAU_YEAR', 'AGE_GROUP']

   data1[x]=data1[x].astype("category")

   
   # Count the number of instances for each target value
   target_value_counts = data1["TARGET"].value_counts()

   # Plot the bar chart
   fig11=plt.figure()
   plt.pie(target_value_counts.values, labels=target_value_counts.index, autopct='%1.1f%%')
   plt.title("Number of Instances by Target Value")
  
   st.pyplot(fig11)

   st.write("Our Data is imbalance so we use undersampling technique to Umbalance the data")
   
   with st.echo():
      
      
      target0=data1[data1["TARGET"]==0]
      target1=data1[data1["TARGET"]==1]
   
      target0=target0.sample(24825)
      data1=pd.concat([target0,target1],axis=0)
   
   st.write(data1["TARGET"].value_counts())
   
   st.subheader("Select Features using information gain")
   
   X=data1.select_dtypes(include="number")
   y=data1["TARGET"]

   X_train,X_test,y_train,y_test=train_test_split(X,y,
    test_size=0.3,
    random_state=0)
   
   with st.echo():
      from sklearn.feature_selection import mutual_info_classif
      # determine the mutual information
      mutual_info = mutual_info_classif(X_train, y_train)
      mutual_info = pd.Series(mutual_info)
      mutual_info.index = X_train.columns
      mutual_info=mutual_info.sort_values(ascending=False)
   
   
   #let's plot the ordered mutual_info values per feature

   fig12=plt.figure()
   sns.barplot(x=mutual_info.index,y=mutual_info.values)
   plt.title("Number of Features that are most relevant")
   plt.xlabel("Target Value")
   plt.xticks(rotation=80,)
   st.pyplot(fig12)
   
   
   with st.echo():
      
      from sklearn.feature_selection import SelectKBest
      #No we Will select the  top 5 important features
      sel_five_cols = SelectKBest(mutual_info_classif, k=5)
      sel_five_cols.fit(X_train, y_train)
      st.write(X_train.columns[sel_five_cols.get_support()])
   
   
   
   from sklearn.preprocessing import LabelEncoder
   le1 = LabelEncoder()
   le2 = LabelEncoder()
   le3 = LabelEncoder()
   le4 = LabelEncoder()
   le5 = LabelEncoder()
   le6 = LabelEncoder()
   le7 = LabelEncoder()
   le8 = LabelEncoder()
   le9 = LabelEncoder()
   le10 = LabelEncoder()
   le11 = LabelEncoder()
   le12 = LabelEncoder()

   categorical_col=data1.select_dtypes(include="category")
   enc=[le1,le2,le3,le4,le5,le6,le7,le8,le9,le10,le11,le12]
   c_list=['NAME_CONTRACT_TYPE','CODE_GENDER', 'NAME_TYPE_SUITE',
       'NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE', 'NAME_FAMILY_STATUS',
       'NAME_HOUSING_TYPE', 'OCCUPATION_TYPE', 'WEEKDAY_APPR_PROCESS_START',
        'ORGANIZATION_TYPE','NAME_CONTRACT_TYPE',"AGE_GROUP"]

   for encoder,column in zip(enc,c_list):
        
      data1[column] = encoder.fit_transform(data1[column].astype(str))
      categorical_col[column] = encoder.fit_transform(categorical_col[column])
   X=categorical_col.iloc[:,1:]
   y=categorical_col["TARGET"]  
   
   
   
   with st.echo():
      ### train Test split is usually done to avaoid overfitting

      X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=100,stratify=y)
      ## Perform chi2 test
      ### chi2 returns 2 values
      ### Fscore and the pvalue
      from sklearn.feature_selection import chi2
      f_p_values=chi2(X_train,y_train)
      p_values=pd.Series(f_p_values[1])
      p_values.index=X_train.columns
      p_values=p_values.sort_values(ascending=False)
      
      fig12=plt.figure()
      sns.barplot(x=p_values.index,y=p_values.values)
      plt.title("Number of Categorical Features that are most relevant")
      plt.xlabel("Target Value")
      plt.xticks(rotation=80,)
      st.pyplot(fig12)
      
      data1.to_csv("cleaned_final_dataset.csv")

   
   
with tab3:
   
   target0=df2[df2["TARGET"]==0]
   target1=df2[df2["TARGET"]==1]
   
   st.header("Bivariate Analysis")
   
   st.markdown("Bivariate analysis is applied in this step, we have applied Univariate (for one variable) and Multivariate (for multiple variables).")
   
   st.write(df2.head())
 
   def plot_countplots_hue(data,col):
     
      fig7=plt.figure(figsize=(12,6))
      sns.countplot(x=col,data=data, hue="TARGET")
      plt.xticks(rotation=45)
      plt.xlabel(col)
      plt.ylabel('Number of loans')
      plt.legend(["Non Defaulted Population(TARGET=0)","Defaulted Population(TARGET=1)"])
      plt.title(f'{col} ')
      st.pyplot(fig7)
      
   plot_countplots_hue(df2,"CODE_GENDER") 
   
    
   st.markdown('The Graph shows that number of Loans in Y-axis and Target 0 or 1 indicating F and M in X-axis, and  different corelated categories are taken and concurrent relationships have been shown.')  
   
   
   plot_countplots_hue(df2,"NAME_CONTRACT_TYPE")
   
    
   st.markdown('This Graph shows number of Loans with contract type i-e cash loans or revolving loans.')
   
   plot_countplots_hue(df2,"NAME_TYPE_SUITE")
 
   st.markdown('This Graph shows number of Loans with suite type.')  
   
   plot_countplots_hue(df2,"NAME_INCOME_TYPE")
   st.markdown('This Graph shows name income type ')  
   
   plot_countplots_hue(df2,"NAME_EDUCATION_TYPE") 
   st.markdown('This Graph shows education type ') 
    
   plot_countplots_hue(df2,"NAME_FAMILY_STATUS")
   st.markdown('This Graph shows family status')  
   
   plot_countplots_hue(df2,"NAME_HOUSING_TYPE")
   st.markdown('This Graph Housing Type ')  
   
   plot_countplots_hue(df2,"OCCUPATION_TYPE")
   st.markdown('This Graph Housing Type ')  
   
   plot_countplots_hue(df2,"CNT_FAM_MEMBERS")
   st.markdown('This Graph Number of member ')  
   
   plot_countplots_hue(df2,"WEEKDAY_APPR_PROCESS_START")
   st.markdown('This Graph Weekdays for process of loans ')  
   
   plot_countplots_hue(df2,"ORGANIZATION_TYPE")
   st.markdown('This Graph Organization Type  ')  
   plot_countplots_hue(df2,"AGE_GROUP")
   st.markdown('6. This Groph shows Age group from very young to senior citizen taking loans.')  
   
   
   
   
   
   st.write("")
   st.write("")
   st.write("")
   st.write("")
   st.subheader("Bi Variate Analysis")
   cmap = sns.color_palette("Set2")
   numerical_col=df2.select_dtypes("number")
   fig, axes = plt.subplots(ncols=2, nrows=5, figsize=(10, 18))
   a = [i for i in axes for i in i] # axes is nested if >1 row & >1 col, need to flatten
   for i, ax in enumerate(a):
      sns.boxplot(x='TARGET', y=numerical_col.columns[i], data=df2, palette=cmap, width=0.5, ax=ax)

   # rotate x-axis for every single plot
   for ax in fig.axes:
      plt.sca(ax)
      plt.xticks(rotation=45)

# set spacing for every subplot, else x-axis will be covered
   plt.tight_layout()
   st.pyplot(fig)
   
   
   fig9=plt.figure(figsize=(12,6))
   sns.violinplot(x=df2["TARGET"],y=df2["DAYS_BIRTH"],hue=df2['AGE_GROUP'])
   plt.xlabel('Class (0: Non-defualted, 1: defualted)')
   plt.ylabel('Age in Years')
   plt.title('Violin Plot of ages by Target')
   st.pyplot(fig9)
   
   
   fig10=plt.figure(figsize=(12,6))
   sns.scatterplot(x='AMT_ANNUITY', y='AMT_CREDIT', data=df2)
   plt.title('Relationship between Fare and Age')
   plt.xlabel('AMT_INCOME_TOTAL')
   plt.ylabel('AMT_CREDIT')
   st.pyplot(fig10)
   
   
   def uni(col):
      
      sns.set(style="darkgrid")
      fig10=plt.figure(figsize=(40,20))
    
   
      plt.subplot(1,2,1)                                   
      sns.distplot(target0[col], color="g" )
      plt.yscale('linear') 
      plt.xlabel(col, fontsize= 30, fontweight="bold")
      plt.ylabel('Non Payment Difficulties', fontsize= 30, fontweight="bold")                    #Target 0
      plt.xticks(rotation=90, fontsize=30)
      plt.yticks(rotation=360, fontsize=30)
     
    
    
    
      plt.subplot(1,2,2)                                                                                                      
      sns.distplot(target1[col], color="r")
      plt.yscale('linear')    
      plt.xlabel(col, fontsize= 30, fontweight="bold")
      plt.ylabel('Payment Difficulties', fontsize= 30, fontweight="bold")                       # Target 1
      plt.xticks(rotation=90, fontsize=30)
      plt.yticks(rotation=360, fontsize=30)
    
      st.pyplot(fig10)
      
      
   uni(col='AMT_ANNUITY')   