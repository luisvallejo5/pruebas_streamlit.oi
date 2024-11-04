import pandas as pd
import streamlit as st 
import streamlit_shadcn_ui as ui
from local_components import card_container
 
#variables
euro_symbol = "$"
 
st.set_page_config(layout="wide", page_title = "Panel de facturación", page_icon=":bar_chart:")
st.title("Panel de facturación")
st.markdown("##")
 
#read data from .csv file
data_previous_year = pd.read_csv("data_2023.csv")
data = pd.read_csv("data_2024.csv")
 
 
#get the month from the date
 
data["Month"] = pd.to_datetime(data["purchase_date"]).dt.month_name()
 
data["Hour"] = pd.to_datetime(data["time"], format= "%H:%M").dt.hour
 
#Filters
cols=st.columns(3)
with cols[0]:
    city = st.multiselect("Selecciona 1s ciudad", options= data["city"].unique().tolist(), default= data["city"].unique().tolist())
with cols[1]:
    gender = st.multiselect("Selecciona el genero", options = data ["gender"].unique().tolist(), default= data["gender"].unique().tolist())
with cols[2]:
    payment_method = st.multiselect("Selecciona el método de pago", options = data["payment_method"].unique().tolist(), default= data["payment_method" ].unique().tolist())
 
#KPIs depending on the filters
data_filtered = data.query(
"`city`== @city & `gender` == @gender & `payment_method` == @payment_method")
 
data_previous_year_filtered = data_previous_year.query(
"`city`== @city & `gender` == @gender & `payment_method` == @payment_method")
 
#KPIs previous year
total_sales_previous_year = round(data_previous_year_filtered ["invoice_amount"].sum(),2)
num_sales_previous_year = data_previous_year_filtered ["invoice_amount"].count()
average_sales_previous_year = round(data_previous_year_filtered ["invoice_amount"].mean() if data_previous_year_filtered ["invoice_amount"].count() != 0 else 0,2)
 
#KPIs current year
total_sales = round(data_filtered["invoice_amount"].sum(),2)
num_sales = data_filtered["invoice_amount"].count()
average_sales = round(data_filtered["invoice_amount"].mean() if data_filtered["invoice_amount"].count() != 0 else 0,2)
 
#Diferencia con el año anterior
 
diff_total_sales = total_sales - total_sales_previous_year
diff_num_sales = num_sales - num_sales_previous_year
diff_average_sales = average_sales - average_sales_previous_year
 
#Calcular la diferencia porcentual
diff_total_sales_percentage = round((diff_total_sales / total_sales_previous_year) * 100, 2) if total_sales_previous_year != 0 else 0
diff_num_sales_percentage = round((diff_num_sales / num_sales_previous_year) * 100, 2) if num_sales_previous_year != 0 else 0
diff_average_sales_percentage = round((diff_average_sales / average_sales_previous_year) * 100, 2) if average_sales_previous_year != 0 else 0
 
#KPIs
st.subheader("KPIs")
cols = st.columns (3)
with cols[0]:
    ui.metric_card (title="Facturación total", content=f"{total_sales:,.2f} {euro_symbol}", description=f"{diff_total_sales_percentage:.2f} % desde el año pasado", key="card1 with cols[1]")
with cols[1]:
    ui.metric_card (title="Ventas totales", content=f"{num_sales:,.0f}", description=f"{diff_num_sales_percentage:.2f}% desde el año pasado", key="card2")
with cols[2]:    
    ui.metric_card (title="Facturación media por transacción", content=f"{average_sales:,.2f} {euro_symbol}", description=str(diff_average_sales_percentage) + "% desde el año pasado")
 
df_selection_month = data_filtered [['Month', 'invoice_amount']].groupby('Month').sum().sort_values (by='invoice_amount', ascending=True).reset_index() 
df_selection_hour= data_filtered [['Hour', 'invoice_amount']].groupby('Hour').sum().sort_values(by='invoice_amount', ascending=True).reset_index()
 
#Cretaing the charts
chart1, chart2 = st.columns (2)
with chart1:
    st.subheader("Ventas por mes")
    with card_container (key="chart1"):
                st.vega_lite_chart (df_selection_month, {'mark': {'type': 'bar', 'tooltip': True, 'fill': 'rgb(50, 250, 100)', 'cornerRadiusEnd': 4},
                    'encoding': {
                        'x': {'field': 'Month', 'type': 'ordinal'},
                        'y': {'field': 'invoice_amount', 'type': 'quantitative', 'axis': {'grid': False}},
                        },
                    },use_container_width=True)
with chart2:
    st.subheader("Ventas por hora")
    with card_container (key="chart2"):
                st.vega_lite_chart (df_selection_hour, {
                    'mark': {'type': 'bar', 'tooltip': True, 'fill': 'rgb(0, 190, 250)', 'cornerRadiusEnd': 4 },
                    'encoding': {
                        'x': {'field': 'Hour', 'type': 'ordinal'},
                        'y': {'field': 'invoice_amount', 'type': 'quantitative', 'axis': {'grid': False}},
                        },
 
                    }, use_container_width=True)
 

#table
st.write("---")
st.subheader("Información de ventas") 
y1,y2,y3 = st.columns(3)
 
with y1:
    choice = ui.select(options = ["2023", "2024"])
with y2:
    st.empty()
with y3:
    st.empty()
if choice == "2023":
    data_filtered = data_previous_year_filtered
 
st.dataframe(data_filtered, use_container_width=True)