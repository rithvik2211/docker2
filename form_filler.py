import pandas as pd
import os
import boto3
from io import BytesIO
from PIL import Image

from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service



print ("Loading Function..")


# Get the service resource
sqs = boto3.resource('sqs', 
                     aws_access_key_id = "AKIAWZ7PWUT5IQOJEOFW",
                     aws_secret_access_key= "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",
                     region_name = 'eu-north-1')

# Get the queue. This returns an SQS.Queue instance
queue = sqs.get_queue_by_name(QueueName='EmailQueue')


print("queue success")
# Message to fill
index = {
  "Fname": "Sandy",
  "Lname": "N",
  "FULLname": "Sandy N",
  "email": "soundharya@chezuba.net",
  "phone": "(317)7321438",
  "subject": "Virtual Volunteering"
}
message1 = "Hey, I came across your organization and was delighted to lean about your efforts. I'd like to speak with you about how we could provide free virtual volunteers to your nonprofit. I eagerly await your response."

#Initialising driver
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
p = './msedgedriver'
path = Service(p)




while True:
    # Process messages by printing out body and optional author name
    for message in queue.receive_messages(MessageAttributeNames=['Author']):
        # Get the custom author message attribute if it was set
        author_text = ''
        #if message.message_attributes is not None:

        link = message.body
        
        # Let the queue know that the message is processed and message is deleted 
        message.delete()

        print("before driver")
        driver = Edge(options=options, service= path)
        driver.maximize_window()
        print("after driver")
        
        #checks if link has http encoding
        if link[:4] == "http":
            url = link
        else:
            url = "http://" + link
        try:
            driver.get(url)
            sleep(2)
        except:
            print("url error")
        
        #opening contact page
        try:
            cont_url = driver.find_element(By.CSS_SELECTOR, value = "a[href *='contact']").get_attribute('href')
            driver.get(cont_url)
        except:
            pass
        
        #checking for formtags 
        try:
            form_tag = driver.find_elements(By.TAG_NAME, "form")
        except:
            pass

        for i in form_tag:
            form_check = i.find_elements(By.TAG_NAME, "input")
            if len(form_check) > 2:
                form_tag = i
                break

        #FILLING EMAIL
        e_check = False

        try:
            temp = form_tag.find_elements(By.CSS_SELECTOR, value = "input[name *='mail'i]")
            if len(temp)>0:
                e_check = True    
        except:
            pass

        if e_check == False:
            try:
                temp = form_tag.find_elements(By.CSS_SELECTOR, value = "input[placeholder *='mail'i]")
                if len(temp)>0:
                    e_check = True               
            except:
                pass
        
        if e_check == False:
            try:
                temp = form_tag.find_elements(By.CSS_SELECTOR, value = "input[type *='email']")
                if len(temp)>0:
                    e_check = True   
            except:
                pass

        try:
            for et in temp:
                try:
                    et.clear
                    et.send_keys(index['email'])
                except:
                    pass
        except:
            pass

        #FILLING FIRST NAME AND LAST NAME
        FN_check = False
        try:
            temp = form_tag.find_element(By.CSS_SELECTOR, value = "input[name *='fname'i]").send_keys(index['Fname'])

            FN_check = True
        except:
            pass
        
        if FN_check == False:
            try:
                temp = form_tag.find_element(By.CSS_SELECTOR, value = "input[name *='first'i]").send_keys(index['Fname'])
                FN_check = True
            except:
                pass
        if FN_check == False:
            try:
                temp = form_tag.find_element(By.CSS_SELECTOR, value = "input[placeholder *='First'i]").send_keys(index['Fname'])
                FN_check = True
            except:
                pass
            
        LN_check = False
        try:
            temp = form_tag.find_element(By.CSS_SELECTOR, value = "input[placeholder *='Last'i]").send_keys(index['Lname'])
            LN_check = True
        except:
            pass    
        if LN_check == False:
            try:
                temp = form_tag.find_element(By.CSS_SELECTOR, value = "input[name *='lname'i]").send_keys(index['Lname'])
                LN_check = True
            except:
                pass

        if LN_check == False:
            try:
                temp = form_tag.find_element(By.CSS_SELECTOR, value = "input[name *='last'i]").send_keys(index['Lname'])
                LN_check = True
            except:
                pass    
        
        
        #FILLING FULL NAME
        if FN_check == False:
            FULN_check = False
            try:
                temp = form_tag.find_element(By.CSS_SELECTOR, value = "input[name *='name'i]").send_keys(index['FULLname'])
                FULN_check = True
            except:
                pass
            if FULN_check == False:
                try:
                    temp = form_tag.find_element(By.CSS_SELECTOR, value = "input[placeholder *='Name'i]").send_keys(index['FULLname'])
                except:
                    pass
        
        
        #FILLING SUBJECT
        sub_check = False    
        try:
            temp = form_tag.find_element(By.CSS_SELECTOR, value = "input[name *='subject'i]").send_keys(index['subject'])
            sub_check = True
        except:
            pass
        if sub_check == False:
            try:
                temp = form_tag.find_element(By.CSS_SELECTOR, value = "input[placeholder *='Subject'i]").send_keys(index['subject'])
                sub_check = True
            except:
                pass
        if sub_check == False:
            try:
                temp = form_tag.find_element(By.CSS_SELECTOR, value = "input[data-aid *='subject'i]").send_keys(index['subject'])
                sub_check = True
            except:
                pass
        
        #FILLING PHONE NUMBER
        
        try:
            temp = form_tag.find_element(By.CSS_SELECTOR, value = "input[placeholder *='Phone'i]").send_keys(index['phone'])
        except:
            pass
        #FILLING MESSAGE
        try:
            temp = form_tag.find_element(By.TAG_NAME, 'textarea')
            temp.send_keys(message1)
        except:
            pass
        
        #SUBMIT BUTTON
        check = False
        try:
            sub = form_tag.find_element(By.CSS_SELECTOR, value = "button[type *= 'submit']").click()
            check = True
        except:
            pass

        if check == False:     
            try:
                sub = form_tag.find_element(By.CSS_SELECTOR, value = "input[type *= 'submit']").click()
                check = True
            except:
                pass
        if check == False:    
            try:    
                sub = form_tag.find_element(By.CSS_SELECTOR, value = "button[data-testid *= 'buttonElement']").click()
                check = True
            except:
                pass
        if check == False:    
            try:    
                sub = form_tag.find_element(By.CSS_SELECTOR, value = "button[type *= 'buttonElement']").click()
                check = True
            except:
                pass

        try:
            if check == True:

                screenshot = driver.find_element(By.TAG_NAME, 'body').screenshot_as_png
                na = link.split(".")
                if "www" in link:
                    ss_name =  na[1] + '.png'
                else:
                    nam = na[0].split('//')
                    ss_name = nam[1]+'.png'


                # with open(ss_name, 'wb') as file:
                #     file.write(screenshot)
                s3 = boto3.client('s3',
                     aws_access_key_id = "AKIAWZ7PWUT5IQOJEOFW",
                     aws_secret_access_key= "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",
                     region_name = 'eu-north-1')
                buffer = BytesIO(screenshot)
                buffer.seek(0)

                bucket_name = 'destinationbucket0-1'
                key = 'form-fill-confirmation/'+ ss_name
                s3.upload_fileobj(buffer, bucket_name, key)

                # with BytesIO(driver.get_screenshot_as_png()) as f:
                #     s3.upload_fileobj(f, bucket_name, key)
                print("later")
        except Exception as err:
            print(err)
            
        try:
            driver.close()
        except Exception as err:
            print(err)




