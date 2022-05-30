import glob
import os

results = os.path.abspath("Akashreddy tallapureddy_Sfdc.pdf")
print("vov",os.path.exists("/Akashreddy tallapureddy_Sfdc.pdf"))
text = "F:/hclresumes/Nandu_rdy.docx"
print(text.find("/"))
x = text.replace("\\","/")
print(x)
print(x.rindex("/"))
real_path = x[0:x.rindex("/")+1]
tier_compns = text[x.rindex("/")+1:]
print(tier_compns)

isFile = os.path.isfile(text)
print(isFile,"--")