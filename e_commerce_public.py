import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


customers_df = pd.read_csv("E-Commerce Public Dataset/customers_dataset.csv")
order_payments_df = pd.read_csv("E-Commerce Public Dataset/order_payments_dataset.csv")
order_items_df = pd.read_csv("E-Commerce Public Dataset/order_items_dataset.csv")
products_df = pd.read_csv("E-Commerce Public Dataset/products_dataset.csv")
product_category_name_translation_df = pd.read_csv("E-Commerce Public Dataset/product_category_name_translation.csv")


st.write(
    """
    # E-Commerce Dashboard
    """
)

st.subheader("Customer Analysis")
top_5_cities = customers_df.groupby(by="customer_city").customer_id.nunique().sort_values(ascending=False).head(5)

plt.figure(figsize=(10,5))
sns.barplot(x=top_5_cities.index, y=top_5_cities.values)
plt.ylabel('Customer Count')
plt.title('Top 5 Cities by Customer Count')
plt.xticks()

st.pyplot(plt)

with st.expander("Description"):
    st.write(
        """The bar plot shows the 5 cities with the highest number of customers
        with Sao Paulo being the city with the highest number of customers. 
        The number of customers coming from Sao Paulo is 15540. This is followed by 
        Rio de Jeneiro (6882 customers) in second place, Belo Horizonte (2773 customers) in third,
          Brasilia (2131 customers) in fourth, and Curitiba (1521 customers) in fifth.
        """
    )

st.subheader("Payment Type Analysis")
payment_type_counts = order_payments_df.groupby(by="payment_type").order_id.count()

plt.figure(figsize=(8, 8))  # Ukuran plot
payment_type_counts.plot(kind='pie', autopct='%1.1f%%')
plt.title('Distribution of Orders by Payment Type')
plt.ylabel('')

st.pyplot(plt)

with st.expander("Description"):
    st.write(
        """The pie chart shows the proportion of payment types used. 
        Credit Card is the most frequently used payment type with a usage percentage of 73.9%. 
        Then, followed by Boleto with a usage percentage of 19%, 
        then Voucher payment type ranks third with a percentage of 5.6%.
        """
    )


order_items_df["shipping_limit_date"] = pd.to_datetime(order_items_df["shipping_limit_date"])
products_df.dropna(axis=0, inplace=True)

order_items_product_df = pd.merge(
    left=products_df,
    right=order_items_df,
    how="outer",
    left_on="product_id",
    right_on="product_id"
)

order_items_product_translation_df = pd.merge(
    left=order_items_product_df,
    right=product_category_name_translation_df,
    how="outer",
    left_on="product_category_name",
    right_on="product_category_name"
)

category_order_counts = order_items_product_translation_df.groupby(by="product_category_name_english").order_id.count().sort_values(ascending=False)

plt.figure(figsize=(12,6)) 
sns.barplot(x=category_order_counts.index, y=category_order_counts.values)
plt.xlabel('Product Category')  
plt.ylabel('Order Count')  
plt.title('Order Count per Product Category')
plt.xticks(rotation=90) 

st.pyplot(plt)

with st.expander("Description"):
    st.write(
        """The bar plot shows the product category and the number of orders. 
        Bed Bath Table is the product category that customers are most interested in.
          So far, the Bed Bath Table category has sold around 11115 orders. 
          then, followed by Health Beauty in second place with 9670 orders, and 
          Sports Leisure in third place with 8641 orders.
        """
    )