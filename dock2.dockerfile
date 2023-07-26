FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-pip
RUN mkdir app
WORKDIR /app
COPY . . 

# ENV key_id = AKIA4BA6NGG3LTRDGWK4
# ENV access_key = 6M1oNjze8zBOZKofs4ypdtuE8VCTRekYXF/b85VK
# ENV region = eu-north-1


RUN pip3 install -r req.txt

RUN apt update
RUN apt install sudo
RUN sudo apt-get update

RUN echo "y" | sudo apt install software-properties-common apt-transport-https wget
RUN wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -
RUN sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main"
RUN echo "y" | sudo apt install microsoft-edge-stable

CMD ["python3", "form_filler.py"]

