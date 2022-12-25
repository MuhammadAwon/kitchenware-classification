# AWS lambda base image
FROM public.ecr.aws/lambda/python:3.9


# Install tflite for aws linux architecture and Pillow for image processing
RUN pip install https://github.com/alexeygrigorev/tflite-aws-lambda/raw/main/tflite/tflite_runtime-2.7.0-cp39-cp39-linux_x86_64.whl
RUN pip install Pillow

# Copy required files to run the app
COPY [ "lambda_function.py", "img_preprocessor.py", "kitchenware-model.tflite", "./" ]

# Expose port to start the server
EXPOSE 8080

# Command to invoke lambda
CMD [ "lambda_function.lambda_handler" ]