# await pyodide.loadPackage("micropip");
# const micropip = pyodide.pyimport("micropip");
# await micropip.install('boto3');
# import boto3

# s3 = boto3.client('s3', aws_access_key_id='AKIA5PDTUHUEBBGAN24X',aws_secret_access_key='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')
# s3.upload_fileobj(img_bytes, bucket_name, key_name)

# print("we made it")

import micropip

async def install_boto3():
    await micropip.install('boto3') 
    package_list = micropip.list()
    print(package_list) 

async def main():
    await install_boto3()

# Call the main function
asyncio.run(main())




# from pyodide import to_js, create_proxy
# pyodide.load_package('boto3')

# s3 = boto3.client('s3', aws_access_key_id='AKIA5PDTUHUEBBGAN24X',aws_secret_access_key='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')
# s3.upload_fileobj(img_bytes, bucket_name, key_name)


            # s3 = pyodide.asgiref.sync.async_to_sync(pyodide.modules['boto3']).client('s3', aws_access_key_id='YOUR_ACCESS_KEY', aws_secret_access_key='YOUR_SECRET_KEY')
            # s3.upload_fileobj(img_bytes, bucket_name, key_name)



  # Upload the image to S3
        # try:
        #     # response = s3.put_object(Bucket=bucket_name, Key=key_name, Body=img_bytes)
        #     # print(response)
        #     s3 = boto3.client('s3', aws_access_key_id='AKIA5PDTUHUEBBGAN24X',aws_secret_access_key='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')
        #     s3.upload_fileobj(img_bytes, bucket_name, key_name)
        # except Exception as e:
        #     print(f"Error uploading image to S3: {e}")

        # def draw_image(self,canvas, x, y, w, h):
        #     self.ctx.drawImage(canvas,x,y,w,h)
