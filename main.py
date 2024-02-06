from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from langchain.chains import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
import datetime
from solarpy import solar_panel
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from fastapi import FastAPI, HTTPException, Query
from fastapi.params import Query
from shapely.geometry import Point
import geopandas as gpd
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import matplotlib.pyplot as plt
from solarpy import solar_panel
import numpy as np
from datetime import datetime
import os
import json
import pyimgur
import re


class Query(BaseModel):
    text: str

class Values(BaseModel):
    data: str

llm = ChatOpenAI(api_key='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')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

count = 0
questions = [
    'Could you provide the approximate size of the area where you plan to install solar panels? (in m^2)',
    'What is the expected current electricity consumption in kilowatt-hours/day (kWh/day) for your property?',
    'Could you share the primary purpose of your solar panel installation to better understand your energy needs? 1- Industrial, 2- Residential',
]

ghi = 1

rrr =[]
def read_info():
    with open('sam.txt', 'r') as f:
        return f.read()

@app.get('/')
def hello():
    return {"hello": 'api'}

@app.post('/response')
def answer(text: Query):
    info = read_info()
    print(info)
    # print(text)
    prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(f"""{info}"""),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{question}"),
        ]
    )

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation = LLMChain(llm=llm, prompt=prompt, verbose=True, memory=memory)

    value = conversation({'question': text.text})['chat_history'][-1]
   
    return {'response': str(value)}
    


file_path = r'./stanford-xx487wn6207-geojson.json'
gdf = gpd.read_file(file_path)

@app.post("/get_data")
async def get_data(data : Query):
    global ghi
    # Create a Point geometry from the given latitude and longitude
    print(data.text)
    arr = data.text.split(',')
    print(arr)

    point = Point(float(arr[0]), float(arr[1]))

    # Check if the point is within any MultiPolygon in the GeoDataFrame
    filtered_data = gdf[gdf.geometry.contains(point)]
    if not filtered_data.empty:

        # Parse the JSON response
        response_dict = json.loads(filtered_data.to_json())
        properties = response_dict["features"][0]["properties"]
        ghi = response_dict["features"][0]["properties"]['annual']
        # Extract data for plotting
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        average_ghi = [properties[month.lower()] for month in months]
        min_ghi = [properties[f"{month.lower()}min"] for month in months]
        max_ghi = [properties[f"{month.lower()}max"] for month in months]

        # Create a plot for minimum, maximum, and normal readings
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(months, min_ghi, label="Min GHI", marker='o')
        ax.plot(months, max_ghi, label="Max GHI", marker='o')
        ax.plot(months, average_ghi, label="Normal GHI", marker='o')

        ax.set_xlabel('Months')
        ax.set_ylabel('GHI Averages')
        ax.set_title('GHI Averages by Month')
        ax.legend()

        # Define the file path for saving the image
        image_file_path = "ghi_averages_plot.png"

        try:
            # Save the plot as an image in the current working directory
            plt.savefig(image_file_path, format='png', bbox_inches='tight')
            plt.close()

            
        except Exception as e:
            return {"error": f"Error while saving the image: {str(e)}"}
    CLIENT_ID = "406e5aeef8c86b3"
    PATH = "ghi_averages_plot.png"

    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    print(uploaded_image.title)
    print(uploaded_image.link)
    print(uploaded_image.size)
    print(uploaded_image.type)

    # If data is found, return GeoJSON properties
    if not filtered_data.empty:
        with open('./data.txt' , 'a') as f:
            data = filtered_data.to_json()
            values = response_dict["features"][0]["properties"]
            for key, value in values.items():
                # f.write(f"{key} : {value}")

                f.write(f"AS per user coordinates {key}: {value} KWh/m^2 of ghi ")
          
            f.close()
            
        
        return {'data':{'data': data , 'image':uploaded_image.link}}
    

    

    
    raise HTTPException(status_code=404, detail="No data found for the specified coordinates.")

@app.post("/solar_power_house")
async def solar_power_house(data: Query):
    
    arr = data.text.split(',')
    panel = solar_panel(2.5, 0.18, id_name='NYC_xmas')
    panel.set_orientation(np.array([0, 0, -1]))
    panel.set_position(float(arr[0]), float(arr[1]), 0)

   
    days_in_month = 28 
    monthly_averages = []

    # Loop through each month
    for i in range(1, 13):
        daily_power = []

        # Loop through each day in the month
        for j in range(1, days_in_month + 1):
            hours = [6, 9, 12, 15, 18]
            daily_power_per_hour = []

            for hour in hours:
                panel.set_datetime(datetime(2019, i, j, hour, 0))
                daily_power_per_hour.append(panel.power())

            daily_average_power = sum(daily_power_per_hour) / len(daily_power_per_hour)
            daily_power.append(daily_average_power)

        monthly_averages.append(sum(daily_power) / 1000)

    # Create a line plot for solar power data
    plt.figure(figsize=(8, 6))
    plt.plot(range(1, 13), monthly_averages, marker='o')
    plt.xlabel('Months')
    plt.ylabel('Solar Power (kW)')
    plt.title('Solar Power Data Visualization')
    
    # Save the plot in the current working directory
    plot_file_path = "solar_power_plot.png"
    plt.savefig(plot_file_path, format='png')
    CLIENT_ID = "406e5aeef8c86b3"
    PATH = "./solar_power_plot1.png"

    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    print(uploaded_image.title)
    print(uploaded_image.link)
    print(uploaded_image.size)
    print(uploaded_image.type)

    

    return {'data':{"monthly_averages": monthly_averages , 'image':uploaded_image.link}}

@app.post("/solar_power_company")
async def solar_power_company(data: Query):
  
    arr = data.text.split(',')
    panel = solar_panel(5, 0.4, id_name='NYC_xmas')
    panel.set_orientation(np.array([0, 0, -1]))
    panel.set_position(float(arr[0]), float(arr[1]), 0)

    days_in_month = 28  
    monthly_averages = []

    
    for i in range(1, 13):
        daily_power = []

        
        for j in range(1, days_in_month + 1):
            hours = [6, 9, 12, 15, 18]
            daily_power_per_hour = []

            for hour in hours:
                panel.set_datetime(datetime(2019, i, j, hour, 0))
                daily_power_per_hour.append(panel.power())

            daily_average_power = sum(daily_power_per_hour) / len(daily_power_per_hour)
            daily_power.append(daily_average_power)

        monthly_averages.append(sum(daily_power) / 1000)

   
    plt.figure(figsize=(8, 6))
    plt.plot(range(1, 13), monthly_averages, marker='o')
    plt.xlabel('Months')
    plt.ylabel('Solar Power (kW)')
    plt.title('Solar Power Data Visualization')
   
    plot_file_path = "solar_power_plot2.png"
    plt.savefig(plot_file_path, format='png')
    CLIENT_ID = "406e5aeef8c86b3"
    PATH = "./solar_power_plot2.png"

    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    print(uploaded_image.title)
    print(uploaded_image.link)
    print(uploaded_image.size)
    print(uploaded_image.type)

    

    return {'data':{"monthly_averages": monthly_averages , 'image':uploaded_image.link}}

@app.post("/solar_power_industry")
async def solar_power_industry(data: Query):
   
    arr = data.text.split(',')
    panel = solar_panel(10, 0.4, id_name='NYC_xmas')
    panel.set_orientation(np.array([0, 0, -1]))
    panel.set_position(float(arr[0]), float(arr[1]), 0)


    days_in_month = 28 
    monthly_averages = []


    for i in range(1, 13):
        daily_power = []

    
        for j in range(1, days_in_month + 1):
            hours = [6, 9, 12, 15, 18]
            daily_power_per_hour = []

            for hour in hours:
                panel.set_datetime(datetime(2019, i, j, hour, 0))
                daily_power_per_hour.append(panel.power())

            daily_average_power = sum(daily_power_per_hour) / len(daily_power_per_hour)
            daily_power.append(daily_average_power)

        monthly_averages.append(sum(daily_power) / 1000)

    plt.figure(figsize=(8, 6))
    plt.plot(range(1, 13), monthly_averages, marker='o')
    plt.xlabel('Months')
    plt.ylabel('Solar Power (kW)')
    plt.title('Solar Power Data Visualization')
    

    plot_file_path = "./solar_power_plot3.png"
    plt.savefig(plot_file_path, format='png')
    CLIENT_ID = "406e5aeef8c86b3"
    PATH = "solar_power_plot3.png"

    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    print(uploaded_image.title)
    print(uploaded_image.link)
    print(uploaded_image.size)
    print(uploaded_image.type)

    

    return {'data':{"monthly_averages": monthly_averages , 'image':uploaded_image.link}}


@app.post('/send_question')
def send_question(text : Query):     
    global count, rrr
    print(count)
    if not count == len(questions):
        curr_question = questions[count]

    rrr.append(text.text)
    print(rrr)
    count += 1
    ans =(rrr[0])
    if count > len(questions):
        count = 0
        
        daily_ene = float(rrr[2])
        optn = float(rrr[3])
        w1 = 370
        w2 = 445
        w3 = 550

        c1 = 12000 
        c2 = 17000 
        c3 = 21000

        num_p1 = int((daily_ene * 1000) / (int(ghi) * w1))
        num_p2 = int((daily_ene * 1000) / (int(ghi) * w2))
        num_p3 = int((daily_ene * 1000) / (int(ghi) * w3))
        print(ghi) 

        size1 = round((w1 * daily_ene) / 1000)
        size2 = round((w2 * daily_ene) / 1000)
        size3 = round((w3 * daily_ene) / 1000)


        cost1 = round(num_p1 * c1)
        cost2 = round(num_p2 * c2)
        cost3 = round(num_p3 * c3)
        if optn == 2 and num_p1<50:
            outpt = (
            f"Option 1:\n"
            f"  - Number of Panels: {num_p1}\n"
            f"  - Panel Size: {size1} square meters\n"
            f"  - Estimated Budget: {cost1} INR\n\n"

            f"Option 2:\n"
            f"  - Number of Panels: {num_p2}\n"
            f"  - Panel Size: {size2} square meters\n"
            f"  - Estimated Budget: {cost2} INR\n\n"  

            f"Option 3:\n"
            f"  - Number of Panels: {num_p3}\n"
            f"  - Panel Size: {size3} square meters\n" 
            f"  - Estimated Budget: {cost3} INR"
        )
        elif optn == 1 and num_p1>100:
             outpt = (
            f"  - Number of Panels: {num_p1}\n"
            f"  - Panel Size: {size1} square meters\n"
            f"  - Estimated Budget: {cost1} INR\n\n"

            f". From our analysis we do not recommend shifting to solar as a primary source of energy for your location"
            )

        else:
            outpt = (
                f"Option 1:\n"
                f"  - Number of Panels: {num_p1}\n"
                f"  - Panel Size: {size1} square meters\n"
                f"  - Estimated Budget: {cost1} INR\n\n"

                f"Option 2:\n"
                f"  - Number of Panels: {num_p2}\n"
                f"  - Panel Size: {size2} square meters\n"
                f"  - Estimated Budget: {cost2} INR\n\n"

                f"Option 3:\n"
                f"  - Number of Panels: {num_p3}\n"
                f"  - Panel Size: {size3} square meters\n"
                f"  - Estimated Budget: {cost3} INR"
            )
        rrr=[]
        return {'question':f'{outpt}'}

    
    print(count)
    return {'question' : f'{curr_question}'}