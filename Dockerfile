FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080
EXPOSE 8080

# Set the OpenAI API key environment variable
ENV OPENAI_API_KEY=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

ENV DISCORD_BOT_TOKEN=MTA5NzE5MjUxMjk2OTUxOTI1NA.GqNFnI.s96ce-cHOWW1CnkIfq_0HrgSlOkEqiwFW4TMGA
# Start the application
CMD ["python", "freelancergpt.py"]
