from django.contrib.auth.models import User
from django.db import models

class brand(models.Model):
    brandID = models.CharField(max_length=8, primary_key=True)
    brandName = models.CharField(max_length=100)
    brandDesc = models.CharField(null=True, blank=True, max_length=8000)
    brandImage = models.CharField(max_length=700, blank=True, null=True)
    brandCoverImage = models.CharField(max_length=700, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now_add=True)


class fabric(models.Model):
    fabricID = models.CharField(primary_key=True, max_length=30)
    fabricName = models.CharField(max_length=100)
    fabricDesc = models.CharField(null=True, blank=True, max_length=8000)
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now_add=True)


class upscaledType(models.Model):
    upscaledTypeID = models.CharField(max_length=50, unique=True)
    upscaledTypName = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now_add=True)


class upscaledProduct(models.Model):
    serialNum = models.AutoField(primary_key=True)
    upscaledID = models.CharField(max_length=100, unique=True)
    upscaledName = models.CharField(max_length=100)
    upscaledDesc = models.CharField(null=True, blank=True, max_length=1000)
    up_productType = models.ForeignKey(upscaledType, on_delete=False)
    upscaledFabricType = models.ForeignKey(fabric, on_delete=False)
    upscaledProductPrice = models.PositiveIntegerField()
    upscaledProductQty = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now_add=True)


class collection(models.Model):
    collectionID = models.CharField(primary_key=True, max_length=100)
    collectionName = models.CharField(max_length=100)
    collectionImage = models.CharField(max_length=700, blank=True, null=True)
    collectionLogoImage = models.CharField(max_length=700, blank=True, null=True)
    collectionCoverImage = models.CharField(max_length=700, blank=True, null=True)
    collectionDesc = models.CharField(null=True, blank=True, max_length=8000)
    brandID = models.ForeignKey(brand, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.collectionName


class category(models.Model):
    categoryID = models.CharField(primary_key=True, max_length=100)
    categoryName = models.CharField(max_length=100)
    categoryDesc = models.CharField(max_length=8000)
    categoryImage = models.CharField(max_length=700, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now_add=True)

class subcategory(models.Model):
    subcategoryID = models.AutoField(primary_key=True, max_length=100)
    categoryID = models.CharField(max_length=100)
    subcategoryName = models.CharField(max_length=100)
    subcategoryDesc = models.CharField(max_length=1000)
    subcategoryImage = models.CharField(max_length=700, blank=True, null=True)
    subcategoryCoverImage = models.CharField(max_length=700, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now_add=True)

class fit_type(models.Model):
    fitTypeID = models.CharField(primary_key=True, max_length=100)
    fitDes = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now_add=True)


class size(models.Model):
    sizeID = models.CharField(primary_key=True, max_length=100)
    sizeDes = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now_add=True)


class product_master(models.Model):
    serialNum = models.AutoField(primary_key=True)
    productID = models.CharField(max_length=100, unique=True)
    productName = models.CharField(max_length=100)
    productDesc = models.CharField(null=True, blank=True, max_length=8000)
    brandID = models.ForeignKey(brand, on_delete=False)
    collectionID = models.ForeignKey(collection, on_delete=False)
    categoryID = models.ForeignKey(category, on_delete=False)
    fabricID = models.ForeignKey(fabric, on_delete=False)
    fitType = models.CharField(max_length=100)
    # size = models.CharField(max_length=100)
    careInstructions = models.CharField(null=True, blank=True, max_length=800)
    keywords = models.CharField(null=True, blank=True, max_length=1000)
    productState = models.BooleanField(default=True)
    productImage = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now_add=True)


class product_price(models.Model):
    # productID = models.ForeignKey(product_master,on_delete=False)
    originalPrice = models.PositiveIntegerField()
    discountRate = models.DecimalField(decimal_places=2, max_digits=5)
    discountPrice = models.DecimalField(decimal_places=2, max_digits=8)
    sellingPrice = models.DecimalField(decimal_places=3, max_digits=8)
    sgst = models.PositiveIntegerField(default=0)
    cgst = models.PositiveIntegerField(default=0)
    igst = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now_add=True)


class product_stock(models.Model):
    # productID = models.ForeignKey(product_master, on_delete=False)
    productQty = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now_add=True)


class ProductVariant(models.Model):
    product = models.ForeignKey(product_master, related_name='variants', on_delete=models.DO_NOTHING, default=None)
    size = models.ForeignKey(size, on_delete=models.DO_NOTHING)
    price = models.OneToOneField(product_price, on_delete=models.DO_NOTHING)
    stock = models.OneToOneField(product_stock, on_delete=models.DO_NOTHING)


class customer_master(models.Model):
    customerID = models.CharField(primary_key=True, max_length=50)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    addLine1 = models.CharField(max_length=500)
    addLine2 = models.CharField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.BigIntegerField()
    country = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    whatsappStatus = models.BooleanField(default=True)
    contactWhatsapp = models.CharField(max_length=50, blank=True, null=True)
    emailID = models.EmailField(max_length=70, null=True, blank=True, unique=True)
    password = models.CharField(max_length=50)


class reseller_master(models.Model):
    resellerID = models.CharField(primary_key=True, max_length=50)
    logoURL = models.CharField(max_length=100)
    companyName = models.CharField(max_length=100)
    gst = models.CharField(max_length=50)
    resellerName = models.CharField(max_length=100)
    rAddLine1 = models.CharField(max_length=500)
    rAddLine2 = models.CharField(max_length=500, blank=True, null=True)
    rCity = models.CharField(max_length=50)
    rState = models.CharField(max_length=50)
    rZip = models.BigIntegerField()
    rCountry = models.CharField(max_length=50)
    addressStatus = models.BooleanField(default=True)
    oAddLine1 = models.CharField(max_length=500, blank=True, null=True)
    oAddLine2 = models.CharField(max_length=500, blank=True, null=True)
    oCity = models.CharField(max_length=50, blank=True, null=True)
    oState = models.CharField(max_length=50, blank=True, null=True)
    oZip = models.BigIntegerField(blank=True, null=True)
    oCountry = models.CharField(max_length=50, blank=True, null=True)
    contact = models.CharField(max_length=50)
    whatsappStatus = models.BooleanField(default=True)
    contactWhatsapp = models.CharField(max_length=50, blank=True, null=True)
    emailID = models.EmailField(max_length=70, null=True, blank=True, unique=True)
    bankName = models.CharField(max_length=200)
    account = models.CharField(max_length=100)
    codeIFSC = models.CharField(max_length=100)


class blog(models.Model):
    blogID = models.CharField(primary_key=True, max_length=50)
    blogImg = models.CharField(null=True, blank=True, max_length=100)
    blogTitle = models.CharField(max_length=200)
    blogDesc = models.CharField(null=True, blank=True, max_length=8000)
    blogStatus = models.BooleanField(default=True)
    blogType = models.CharField(null=True, blank=True, max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now_add=True)


class websitemessages(models.Model):
    webID = models.CharField(primary_key=True, max_length=50)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    contact = models.CharField(max_length=50)
    emailID = models.EmailField(max_length=70, null=True, blank=True, unique=True)
    message = models.CharField(max_length=500)
    status = models.CharField(max_length=50)
    reason = models.CharField(max_length=200)
