from .models import *
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from firebase import Firebase
import json
import python_jwt as jwt
import datetime
import facebook
tz = datetime.datetime.now()
count = 0

config = {
             "apiKey": "AIzaSyDDs3_YwJwCERwIB_zguxKVNZpmsSCSEBc",
             "authDomain": "sugandh-9a9db.firebaseapp.com",
             "databaseURL": "https://sugandh-9a9db.firebaseio.com",
             "storageBucket": "sugandh-9a9db.appspot.com"
         }

def index(request):
    full_list = []
    customerobj = customer_master.objects.all()
    for customer in customerobj:
        l = []
        l.append(customer.firstName)
        l.append(customer.contact)
        full_list.append(l)

    json_form = json.dumps(full_list)
    print(json_form)
    output = {
        'customerobj':customerobj,
        'json_form':json_form,

    }
    return render(request,"index.html",output)

# About us
def aboutus(request):
    firebase = Firebase(config)
    db = firebase.database()
    x = db.child("About Us").get()
    output = {
        'value': x,
    }
    return render(request,"about-us.html",output)

# update about us
def updateaboutus(request):
    if (request.method == 'POST'):
        Introduction = request.POST.get("Introductio")
        Definition = request.POST.get("Definitio")
        Information = request.POST.get("Informatio")
        WelcomeSugandh = request.POST.get("WelcomeSugandh")
        ContactSugandh = request.POST.get("ContactSugandh")
        firebase = Firebase(config)
        db = firebase.database()
        x = db.child("About Us").update({'Introduction':Introduction,'Definition':Definition,'Information':Information,'WelcomeSugandh':WelcomeSugandh,'ContactSugandh':ContactSugandh})
    return redirect("/About-Us")

def globalsetting(request):
    return render(request, "global-setting.html",{})


# view of collection febri and size
def showcoll(request):
    collectionobj = collection.objects.all()
    fabricobj = fabric.objects.all()
    sizeobj = size.objects.all()
    output = {
        'collectionobj':collectionobj,
        'fabricobj':fabricobj,
        'sizeobj':sizeobj
    }
    return render(request, "collection.html", output)

# delete collection
def deletecoll(request,collectionID):
    collectionobj = collection.objects.filter(collectionID = collectionID)
    collectionobj.delete()
    return redirect("/collection.html")

# update collection
def updatecoll(request):
    if (request.method == 'POST'):
        id = request.POST.get("collection_id")
        coll_name = request.POST.get("collection_name")
        coll_desc = request.POST.get("collection_desc")
        filepath = request.FILES.getlist('imgname')   # collection img
        coverimg = request.FILES.getlist('coverimg')    # collection coverimg

        print("================collection img-=============",filepath)
        print("================collection coverimg==================",coverimg)

        # firebase = Firebase(config)
        # storage = firebase.storage()
        # for i in range(len(filepath)):
        #     storage.child("Collections/" + coll_name + "/" + str(filepath[i])).put(filepath[i])
        #     filepath = storage.child("Collections/" + coll_name + "/" + str(filepath[i])).get_url(token='null')
        #
        # for j in range(len(coverimg)):
        #     storage.child("Collections/Inside_banner/" + str(coverimg[j])).put(coverimg[j])
        #     coverimg = storage.child("Collection/Inside_banner/" + str(coverimg[j])).get_url(token='null')
        #
        # collection.objects.filter(collectionID=id).update(collectionName=coll_name,collectionDesc=coll_desc,collectionImage=filepath,collectionCoverImage=coverimg,lastUpdated = tz)
        return redirect("/collection.html")

# add collection
def addcoll(request):
    collectionobj = collection.objects.all().order_by('-collectionID')[:1]
    x = ""
    for coll in collectionobj:
        x =coll.collectionID
    x = int(x[3:])+1
    Cid = 'COL'+str(x).zfill(3)

    if (request.method == 'POST'):
         cname = request.POST.get('collection_na')
         cdesc = request.POST.get('collectiond')
         filepath = request.FILES.getlist('imgname')    # collection img
         coverimg = request.FILES.getlist('coverimg')    # collection coverimg
         firebase = Firebase(config)
         storage = firebase.storage()
         for i in range(len(filepath)):
             storage.child("Collections/" + cname + "/" + str(filepath[i])).put(filepath[i])
             filepath = storage.child("Collections/" + cname + "/" + str(filepath[i])).get_url(token='null')

         for j in range(len(coverimg)):
             storage.child("Collections/Inside_banner/" + str(coverimg[j])).put(coverimg[j])
             coverimg = storage.child("Collection/Inside_banner/" + str(coverimg[j])).get_url(token='null')

         collection.objects.create(
             collectionID=Cid,
             collectionName=cname,
             collectionDesc=cdesc,
             collectionImage=filepath,
             collectionCoverImage=coverimg,
             brandID=brand.objects.only('brandID').get(brandID = 'B001'),
             created= tz,
             lastUpdated = tz
         )
    return redirect("/collection.html")

# delete s
def deletesize(request,sizeID):
    sizeobj = size.objects.get(sizeID=sizeID)
    sizeobj.delete()
    return redirect("/collection.html")

# update size
def updatesize(request):
    if (request.method == 'POST'):
        sizedes = request.POST.get('size_name')
        id = request.POST.get('size')
        size.objects.filter(sizeID=id).update(sizeDes = sizedes,lastUpdated =tz)
        return redirect("/collection.html")

# ass size
def addsize(request):
    if (request.method == 'POST'):
        sid = request.POST.get('size_id')
        sname = request.POST.get('size_na')
        size.objects.create(
            sizeID=sid,
            sizeDes=sname,
            created=tz,
            lastUpdated=tz
        )
    return redirect("/collection.html")

# delete fabric
def deletefabric(request,fabricID):
    febricobj = fabric.objects.get(fabricID = fabricID)
    febricobj.delete()
    return redirect("/collection.html")

# update fabric
def updatefabric(request):
    id = request.POST.get('fabric_id')
    fabric_name = request.POST.get('fabric_name')
    fabric_desc = request.POST.get('fabric_desc')
    fabric.objects.filter(fabricID=id).update(fabricName=fabric_name,fabricDesc=fabric_desc,lastUpdated =tz)
    return redirect("/collection.html")

# add fabric
def addfabric(request):
    fabricobj = fabric.objects.all().order_by('-fabricID')[:1]
    x = ""
    for fab in fabricobj:
        x = fab.fabricID
    x = int(x[1:]) + 1
    Fid = 'F' + str(x).zfill(4)

    if (request.method == 'POST'):
         fname = request.POST.get('fabric_na')
         fdesc = request.POST.get('fabric_de')
         fabric.objects.create(
             fabricID=Fid,
             fabricName=fname,
             fabricDesc=fdesc,
             lastUpdated =tz
         )
    return redirect("/collection.html")

# view product
def showproduct(request):
    productobj = product_master.objects.select_related('collectionID','brandID', 'categoryID', 'fabricID')
    # pagination
    paginator = Paginator(productobj, 20)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)

    priceobj = product_price.objects.all()
    fabricobj = fabric.objects.all()
    fit_typeobj = fit_type.objects.all()
    categoryobj = category.objects.all()
    all_sizes = size.objects.filter(productvariant__product=productobj)

    context = {
        'productobj':productobj,
        'fabricobj':fabricobj,
        'fit_typeobj':fit_typeobj,
        'priceobj':priceobj,
        'categoryobj':categoryobj,
        'all_sizes':all_sizes,
        'contacts':contacts
    }
    return render(request, "product.html", context)

# delete product
def deleteproduct(request,productID):
    productobj = product_master.objects.get(productID = productID)
    productobj_id = product_master.objects.get(productID = productID).serialNum
    productvariantobj = ProductVariant.objects.get(product = productobj_id)
    productvariantobj.delete()
    productobj.delete()
    global z
    z = z - 1
    if(z <= 0):
        return redirect("/product.html")
    else:
        return redirect("/display.html")

# update product
def updateproduct(request):
    if (request.method == 'POST'):
        sno = request.POST.get("Serial no")
        cname = request.POST.get('Collection Name')
        pname = request.POST.get('Product Name')
        pcategory = request.POST.get('Category')
        pdesc = request.POST.get('Product Description')
        careins = request.POST.get('Care Instructions')
        psize = request.POST.get('size')
        size_id = size.objects.get(sizeID=psize)
        fabricn = request.POST.get('fabric')
        fittype = request.POST.get('fselect')
        displays = request.POST.get('display')
        pprice = int(request.POST.get('Product Price'))
        pqty = int(request.POST.get('Available Quantity'))
        if (displays == 'on'):
            displays = 1
        else:
            displays = 0

        fabricid = fabric.objects.filter(fabricName = fabricn)
        for fabr in fabricid:
            fabricid = fabr.fabricID

        # brandid = brand.objects.filter(brandName = bname)
        # for bran in brandid:
        #     brandid = bran.brandID

        categoryid = category.objects.filter(categoryName = pcategory)
        for cat in categoryid:
            categoryid = cat.categoryID

        collectionid = collection.objects.filter(collectionName = cname)
        for coll in collectionid:
            collectionid = coll.collectionID

        stock_no = ProductVariant.objects.get(product = sno).stock.id
        price_no = ProductVariant.objects.get(product = sno).price.id
        product_master.objects.filter(serialNum=sno).update(productName = pname, productDesc = pdesc,collectionID = collectionid,categoryID = categoryid,fabricID = fabricid,fitType = fittype,careInstructions = careins,productState = displays,lastUpdated = tz )
        product_stock.objects.filter(id = stock_no).update(productQty = pqty)
        product_price.objects.filter(id = price_no).update(originalPrice = pprice)
        ProductVariant.objects.filter(product=sno).update(size=size_id)

    return redirect("/display.html")

# view reseller
def showreseller(request):
    resellerobj = reseller_master.objects.all()
    return render(request, "reseller.html", {'resellerobj':resellerobj})

# delete reseller
def deletereseller(request,resellerID):
    resellerobj = reseller_master.objects.get(resellerID = resellerID)
    resellerobj.delete()
    return redirect("/reseller.html")

# update reseller
def updatereseller(request):
    if (request.method == 'POST'):
        gst = request.POST.get('GST Number')
        cname = request.POST.get('Company Name')
        rname = request.POST.get('Contact Person Name')
        oa1 = request.POST.get('Office Address Line 1')
        oa2 = request.POST.get('Office Address Line 2')
        op = request.POST.get('oPincode')
        oc = request.POST.get('City')
        os = request.POST.get('State')
        oco = request.POST.get('Country')
        da1 = request.POST.get('Delivery Address Line 1')
        da2 = request.POST.get('Delivery Address Line 2')
        ds = request.POST.get('dState')
        dc = request.POST.get('dCity')
        dco = request.POST.get('dCountry')
        dp = request.POST.get('dPincode')
        pno = request.POST.get('Primary Contact Number')
        wno = request.POST.get('Whatsapp Number')
        eid = request.POST.get('Email ID')
        bname = request.POST.get('Bank Name')
        ano = request.POST.get('Account Number')
        ifsc = request.POST.get('IFSC Code')
        rid = request.POST.get('reseller id')
        if not op:
            op = 0
        if not dp:
            dp = 0

        addreestatus = request.POST.get('addressst')
        if (addreestatus == 'on'):
            addreestatus = 1
        else:
            addreestatus = 0

        ws = request.POST.get('wstatus')
        if (ws == 'on'):
            wstatus = 1
        else:
            wstatus = 0

        if (addreestatus == 1):
            if (wstatus == 1):
                reseller_master.objects.filter(resellerID=rid).update(companyName=cname, gst=gst, resellerName=rname,
                                               rAddLine1=oa1, rAddLine2=oa2, rCity=oc, rState=os, rZip=op,
                                               rCountry=oco, oAddLine1=oa1, oAddLine2=oa2, oCity=oc,
                                               oState=os, oZip=op, oCountry=oco, contact=pno,
                                               contactWhatsapp=pno,
                                               emailID=eid, bankName=bname, account=ano, codeIFSC=ifsc,
                                               addressStatus=addreestatus, whatsappStatus=wstatus)
            elif (wstatus == 0):
                reseller_master.objects.filter(resellerID=rid).update(companyName=cname, gst=gst, resellerName=rname,
                                               rAddLine1=oa1, rAddLine2=oa2, rCity=oc, rState=os, rZip=op,
                                               rCountry=oco, oAddLine1=oa1, oAddLine2=oa2, oCity=oc,
                                               oState=os, oZip=op, oCountry=oco, contact=pno,contactWhatsapp=wno,
                                               emailID=eid, bankName=bname, account=ano, codeIFSC=ifsc,
                                               addressStatus=addreestatus, whatsappStatus=wstatus)
        elif (addreestatus == 0):
            if (wstatus == 1):
                reseller_master.objects.filter(resellerID=rid).update(companyName=cname, gst=gst, resellerName=rname,rAddLine1=da1,
                                               rAddLine2=da2, rCity=dc, rState=ds, rZip=dp, rCountry=dco,
                                               oAddLine1=oa1, oAddLine2=oa2, oCity=oc, oState=os, oZip=op,
                                               oCountry=oco, contact=pno, contactWhatsapp=pno, emailID=eid,
                                               bankName=bname, account=ano, codeIFSC=ifsc, addressStatus=addreestatus, whatsappStatus=wstatus)
            elif (wstatus == 0):
                reseller_master.objects.filter(resellerID=rid).update(companyName=cname, gst=gst, resellerName=rname,rAddLine1=da1,
                                               rAddLine2=da2, rCity=dc, rState=ds, rZip=dp, rCountry=dc,
                                               oAddLine1=oa1, oAddLine2=oa2, oCity=oc, oState=os, oZip=op,
                                               oCountry=oco, contact=pno, contactWhatsapp=wno, emailID=eid,
                                               bankName=bname, account=ano, codeIFSC=ifsc, addressStatus=addreestatus, whatsappStatus=wstatus)


    return redirect("/reseller.html")

# add reseller
def addreseller(request):
    return render(request, "add-reseller.html", {})

# add reseller detail
def addresellerdetail(request):
    resellerobj = reseller_master.objects.all().order_by('-resellerID')[:1]
    x = ""
    for reseller in resellerobj:
        x = reseller.resellerID
    x = int(x[3:]) + 1
    Rid = 'RS' + str(x).zfill(3)
    if (request.method == 'POST'):
        addreestatus = request.POST.get('address')
        if (addreestatus == 'on'):
            addreestatus = 1
        else:
            addreestatus = 0
        ws = request.POST.get('ws')
        if(ws == 'on'):
            wstatus = 1
        else:
            wstatus = 0
        gst = request.POST.get('GST Number')
        cname = request.POST.get('Company Name')
        rname = request.POST.get('Contact Person Name')
        oa1 = request.POST.get('Office Address Line 1')
        oa2 = request.POST.get('Office Address Line 2')
        opin = request.POST.get('oPincode')
        ocity = request.POST.get('oCity')
        ostate = request.POST.get('oState')
        ocuntry = request.POST.get('oCountry')
        da1 = request.POST.get('Delivery Address Line 1')
        da2 = request.POST.get('Delivery Address Line 2')
        dpin = request.POST.get('dPincode')
        dcity = request.POST.get('dCity')
        dstate = request.POST.get('dState')
        dcountry = request.POST.get('dCountry')
        phone = request.POST.get('Primary Contact Number')
        wno = request.POST.get('Whatsapp Number')
        email = request.POST.get('Email ID')
        bname = request.POST.get('Bank Name')
        ano = request.POST.get('Account Number')
        ifsc = request.POST.get('IFSC Code')

        if(addreestatus == 1):
            if(wstatus == 1):
                reseller_master.objects.create(resellerID = Rid,companyName = cname,gst = gst , resellerName = rname ,
                                           rAddLine1 = oa1, rAddLine2 = oa2 , rCity = ocity, rState = ostate, rZip = opin,
                                           rCountry = ocuntry , oAddLine1 = oa1, oAddLine2 = oa2, oCity = ocity ,
                                           oState = ostate,oZip = opin,oCountry = ocuntry,contact = phone, contactWhatsapp = phone,
                                           emailID = email, bankName = bname, account = ano, codeIFSC =ifsc, addressStatus = addreestatus,whatsappStatus=wstatus )
            elif(wstatus == 0):
                reseller_master.objects.create(resellerID=Rid, companyName=cname, gst=gst, resellerName=rname,
                                               rAddLine1=oa1, rAddLine2=oa2, rCity=ocity, rState=ostate, rZip=opin,
                                               rCountry=ocuntry, oAddLine1=oa1, oAddLine2=oa2, oCity=ocity,
                                               oState=ostate, oZip=opin, oCountry=ocuntry, contact=phone, contactWhatsapp=wno,
                                               emailID=email, bankName=bname, account=ano, codeIFSC=ifsc,
                                               addressStatus=addreestatus,whatsappStatus=wstatus)
        elif(addreestatus == 0):
            if(wstatus == 1):
                reseller_master.objects.create(resellerID=Rid, companyName=cname, gst=gst, resellerName=rname, rAddLine1=da1,
                                           rAddLine2=da2, rCity=dcity, rState=dstate, rZip=dpin, rCountry=dcountry,
                                           oAddLine1=oa1, oAddLine2=oa2, oCity=ocity, oState=ostate, oZip=opin,
                                           oCountry=ocuntry, contact=phone, contactWhatsapp=phone, emailID=email,
                                           bankName=bname, account=ano, codeIFSC=ifsc,addressStatus=addreestatus,whatsappStatus=wstatus)
            elif(wstatus == 0):
                reseller_master.objects.create(resellerID=Rid, companyName=cname, gst=gst, resellerName=rname,rAddLine1=da1,
                                               rAddLine2=da2, rCity=dcity, rState=dstate, rZip=dpin, rCountry=dcountry,
                                               oAddLine1=oa1, oAddLine2=oa2, oCity=ocity, oState=ostate, oZip=opin,
                                               oCountry=ocuntry, contact=phone, contactWhatsapp=wno, emailID=email,
                                               bankName=bname, account=ano, codeIFSC=ifsc, addressStatus=addreestatus,whatsappStatus=wstatus)

    return render(request, "reseller.html", {})

# view blogs
def showblogs(request):
    blogsobj = blog.objects.all()
    return render(request,"blogs.html", {'blogsobj':blogsobj})

# delete blogs
def deleteblog(request,blogID):
    blogsobj = blog.objects.filter(blogID = blogID)
    blogsobj.delete()
    return redirect("/blogs.html")

# add blog
def addblog(request):
    return render(request, "add-blogs.html", {})

# add blog detail
def addblogdetail(request):
    blogobj = blog.objects.all().order_by('-blogID')[:1]
    x = ""
    for blogs in blogobj:
        x = blogs.blogID
    x = int(x[3:]) + 1
    Bid = 'BL' + str(x).zfill(4)
    if (request.method == 'POST'):
        btitle = request.POST.get('Blog Title')
        bdesc = request.POST.get("Description")
        bstatus = request.POST.get("Blog State")
        btype = request.POST.get('Blog Type')
        if(bstatus == 'on'):
            bstatus = 1
        else:
            bstatus = 0

        filepath = request.FILES.getlist('imgname')

        firebase = Firebase(config)
        storage = firebase.storage()
        imgurl = []
        for i in range(len(filepath)):
            storage.child("Blogs/"+str(filepath[i])).put(filepath[i])
            imgurl = storage.child("Blogs/"+str(filepath[i])).get_url(token='null')

        blog.objects.create(blogID=Bid,blogTitle=btitle,blogDesc=bdesc,blogImg=imgurl,blogStatus=bstatus,blogType=btype,
                            created=tz,lastUpdated=tz)

    return redirect("/blogs.html")


# update blog
def updateblog(request):
    if (request.method == 'POST'):
        id = request.POST.get("Blog Id")
        blogt = request.POST.get("Blog Titl1")
        blogd = request.POST.get("Descriptio1")
        bstatus = request.POST.get('BlogState')
        btype = request.POST.get('Blogtyp')
        if(bstatus == 'on'):
            bstatus = 1
        else:
            bstatus = 0

        blog.objects.filter(blogID=id).update(blogTitle=blogt,blogDesc=blogd,blogStatus=bstatus,blogType=btype,lastUpdated = tz)
        return redirect("/blogs.html")

# add product
def addproduct(request):
    collectionobj = collection.objects.all()
    context  = {
        'collectionobj':collectionobj,
    }
    return render(request, "collection-details.html", context)

def productdetail(request):
    if (request.method == 'POST'):
        global z
        z = 0
        collnd = request.POST.get('collectionname').split("'#'")
        global cname
        cname = collnd[1]
        global cdes
        cdes = collnd[0]
        fabricobj = fabric.objects.all()
        fit_typeobj = fit_type.objects.all()
        sizeobj = size.objects.all()
        categoryobj = category.objects.all()
        brandobj = brand.objects.all()
        context = {
            'fabricobj': fabricobj,
            'fit_typeobj':fit_typeobj,
            'sizeobj':sizeobj,
            'categoryobj':categoryobj,
            'brandobj':brandobj,
        }
    return render(request, "product-details.html",context)




def storeproduct(request):
    fabricobj = fabric.objects.all()
    fit_typeobj = fit_type.objects.all()
    sizeobj = size.objects.all()
    categoryobj = category.objects.all()
    brandobj = brand.objects.all()
    context = {
        'fabricobj': fabricobj,
        'fit_typeobj': fit_typeobj,
        'sizeobj': sizeobj,
        'categoryobj': categoryobj,
        'brandobj':brandobj,
    }
    global z
    z = z+1
    productobj = product_master.objects.all().order_by('-productID')[:1]
    x = ""
    for product in productobj:
        x = product.productID
    x = int(x[4:]) + 1
    Pid = 'WOS-' + str(x)
    if(request.method == 'POST'):
        pname = request.POST.get('Product Name')
        pdes = request.POST.get('Product Description')
        pcata = request.POST.get('Category')
        fabricname = request.POST.get('fabric')
        fittype = request.POST.get('fit type')
        care = request.POST.get('Care Instructions')
        size_id = request.POST.get('size')
        size_id = size.objects.get(sizeID = size_id)
        pprice = request.POST.get('Product Price')
        aquantity = request.POST.get('Available Quantity')
        dstatus = request.POST.get('displaystate')
        brandd = request.POST.get('brandn')
        filepath = request.FILES.getlist('imgname')

        firebase = Firebase(config)
        storage = firebase.storage()
        finalimglist = []
        imglist = []
        for i in range(len(filepath)):
            storage.child("Product/"+cname+"/"+str(filepath[i])).put(filepath[i])
            imgurl = storage.child("Product/"+cname+"/"+str(filepath[i])).get_url(token='null')
            imglist.append(imgurl)

        finalimglist.append(imglist)

        brandid = brand.objects.filter(brandName = brandd)
        for bran in brandid:
            brandid = bran.brandID
            brandid = brand.objects.get(brandID=brandid)

        fabricid = fabric.objects.filter(fabricName=fabricname)
        for fabr in fabricid:
            fabricid = fabr.fabricID
            fabricid = fabric.objects.get(fabricID = fabricid)

        categoryid = category.objects.filter(categoryName=pcata)
        for cat in categoryid:
            categoryid = cat.categoryID
            categoryid = category.objects.get(categoryID = categoryid)

        collectionid = collection.objects.filter(collectionName=cname)
        for coll in collectionid:
            collectionid = coll.collectionID
            collectionid = collection.objects.get(collectionID = collectionid)

        if (dstatus == 'on'):
            dstatus = 1
        else:
            dstatus = 0

        product_master.objects.create(productID = Pid,productName = pname, productDesc = pdes,brandID = brandid,collectionID = collectionid,categoryID = categoryid,fabricID = fabricid,fitType = fittype,careInstructions = care,productImage =finalimglist,productState = dstatus,created = tz,lastUpdated = tz )
        product_id = product_master.objects.latest('serialNum')
        product_price.objects.create(originalPrice = pprice ,discountRate = 0.00,discountPrice = 0.00,sellingPrice = 0.000,created = tz,lastUpdated= tz,sgst = 0, cgst = 0, igst = 0)
        product_stock.objects.create(productQty =aquantity, created=tz, lastUpdated=tz)
        product_price_id = product_price.objects.latest('id')
        product_stock_id = product_stock.objects.latest('id')
        ProductVariant.objects.create(product = product_id,size = size_id,price = product_price_id,stock = product_stock_id)
    return render(request,"product-details.html",context)

def display(request):
    fabricobj = fabric.objects.all()
    fit_typeobj = fit_type.objects.all()
    sizeobj = size.objects.all()
    categoryobj = category.objects.all()
    brandobj = brand.objects.all()
    productobj = product_master.objects.all().order_by('-productID')[:z]
    ProductVariantobj = ProductVariant.objects.all().order_by('-id')[:z]
    context = zip(productobj,ProductVariantobj)
    return render(request,"display.html",{'context':context,'fabricobj': fabricobj,'fit_typeobj': fit_typeobj,'sizeobj': sizeobj,'categoryobj': categoryobj,'brandobj':brandobj})

def finish(request):
    return render(request,"finish.html",{})

# add product detail
def addproductdetail(request):
    if (request.method == 'POST'):
        cname = request.POST.get('collectionname')
        cname = cname.split("'#'")
        cid = collection.objects.get(collectionName=cname[1])
        pname = request.POST.get('Product Name')
        pdes = request.POST.get('Product Description')
        fabricname = request.POST.get('fabric')
        fabricid = fabric.objects.get(fabricName = fabricname)
        fittype = request.POST.get('fit type')
        categoryname = request.POST.get('Category')
        categoryid = category.objects.get(categoryName = categoryname)
        care = request.POST.get('Care Instructions')
        size = request.POST.get('size')
        pprice = request.POST.get('Product Price')
        aquantity = request.POST.get('Available Quantity')

        # product_master.objects.create(
        #     collectionID = cid,
        #
        # )

        return redirect("/product.html")

# view customers
def customer(request):
    customer_masterobj = customer_master.objects.all()
    return render(request, "customers.html", {'customer_masterobj':customer_masterobj})

def updatecustomer(request):
    if (request.method == 'POST'):
        id = request.POST.get('Customer Id')
        fname = request.POST.get('First Name')
        lname = request.POST.get('Last Name')
        add1 = request.POST.get('Address Line 1')
        add2 = request.POST.get('Address Line 2')
        city = request.POST.get('City')
        state = request.POST.get('State')
        zip = request.POST.get('Zip')
        country = request.POST.get('Country')
        contact = request.POST.get('Contact')
        wcontact = request.POST.get('Contactwhatsapp')
        eid = request.POST.get('Email id')
        passw = request.POST.get('password')
        wstatus = request.POST.get('displaystate')
        if (wstatus == 'on'):
            wstatus = 1
        else:
            wstatus = 0

        customer_master.objects.filter(customerID = id ).update(firstName = fname, lastName = lname , addLine1 = add1, addLine2 = add2,city = city, state = state, zip = zip, country = country, contact = contact , whatsappStatus = wstatus ,contactWhatsapp = wcontact, emailID = eid,password = passw)


    return redirect("/customers.html")

# view customer detail
def customerdetail(request,customerID):
    return render(request, "customers-details.html", {})


def push(request):
    token = 'EAAdTgAjm4mIBALEZB5ty9p1i79QfPO1L6GD1t7ABVSJ5V2wnVu4wZAgs4LA3ZA4Sj6iZBlsmYCjktb4idcbaZAMiecEnvfcyxBzA78zerzl8bmStC6wi13kUX3V7eZAOgqTfU7qA0HjzfrlZA8DdEHbBux83HePZBQEZD'

    fb = facebook.GraphAPI(access_token=token)
    fb.put_object(parent_object='me', connection_name='feed', message = 'test')
    return redirect("/customer.html")

def showwebsitemessage(request):
    webmessageobj = websitemessages.objects.all()

    return render(request, "websitemessage.html", {'webmessageobj':webmessageobj})

def updatewebmsg(request):
    if (request.method == 'POST'):
        id = request.POST.get('Id')
        status = request.POST.get('Status')
        reason = request.POST.get('Reason')

        websitemessages.objects.filter(webID=id).update(status = status,reason = reason)
        return redirect("/websitemessage.html")

def deletewebmsg(request,webID):
    webmsgobj = websitemessages.objects.filter(webID=webID)
    webmsgobj.delete()
    return redirect("/websitemessage.html")

# brand
def showbrand(request):
    brandobj = brand.objects.all()
    return render(request,"brand.html",{'brandobj':brandobj})


def addbrand(request):
    if (request.method == 'POST'):
        bname = request.POST.get('Brand_name')
        bdesc = request.POST.get('Brand_Description')
        filepath = request.FILES.getlist('imgname')
        coverimg = request.FILES.getlist('coverimg')
        brandobj = brand.objects.all().order_by('-brandID')[:1]
        x = ""
        for brands in brandobj:
            x = brands.brandID
        x = int(x[3:]) + 1
        Bid = 'B' + str(x).zfill(3)

        firebase = Firebase(config)
        storage = firebase.storage()

        for i in range(len(filepath)):
            storage.child("Brands/" + "Brand_logo/" + str(coverimg[i])).put(coverimg[i])
            imgurl = storage.child("Brands/" + "Brand_logo/" + str(coverimg[i])).get_url(token='null')

        for j in range(len(coverimg)):
            storage.child("Brands/" + str(filepath[j])).put(filepath[i])
            coverimg = storage.child("Brands/" + str(filepath[i])).get_url(token='null')


        brand.objects.create(brandID=Bid, brandName=bname, brandDesc=bdesc, brandImage=imgurl, brandCoverImage=coverimg, created=tz,
                             lastUpdated=tz)

    return redirect("/brand.html")


def updatebrand(request):
    if (request.method == 'POST'):
        id = request.POST.get('Id')
        bname = request.POST.get('Brand Name')
        bdesc = request.POST.get('Brand Description')
        filepath = request.FILES.getlist('imgname')
        coverimg = request.FILES.getlist('coverimg')

        print("========================img==================",filepath)
        print("=====================cover=====================",coverimg)

        brand.objects.filter(brandID=id).update(brandName=bname, brandDesc=bdesc)
        # firebase = Firebase(config)
        # storage = firebase.storage()
        #
        # for i in range(len(filepath)):
        #     storage.child("Brands/" + "Brand_logo/" + str(coverimg[i])).put(coverimg[i])
        #     imgurl = storage.child("Brands/" + "Brand_logo/" + str(coverimg[i])).get_url(token='null')
        #
        # for j in range(len(coverimg)):
        #     storage.child("Brands/" + str(filepath[j])).put(filepath[i])
        #     coverimg = storage.child("Brands/" + str(filepath[i])).get_url(token='null')
        #
        #
        # brand.objects.filter(brandID=id).update(brandName=bname,brandDesc=bdesc, brandImage=imgurl, brandCoverImage=coverimg,created = tz,lastUpdated = tz)
        return redirect("/brand.html")

def deletebrand(request,brandID):
    brandobj = brand.objects.filter(brandID=brandID)
    brandobj.delete()
    return redirect("/brand.html")

def setting_coll(request):
    if (request.method == 'POST'):
        filepath = request.FILES.getlist('imgname')

        firebase = Firebase(config)
        storage = firebase.storage()
        for i in range(len(filepath)):
            storage.child("setting/Collection Page/collection.jpg").put(filepath[i])


        return redirect("/setting.html")


def setting_women(request):
    if(request.method == 'POST'):
        filepath = request.FILES.getlist('imgname')

        firebase = Firebase(config)
        storage = firebase.storage()
        for i in range(len(filepath)):
            storage.child("setting/Women Page/women.jpg").put(filepath[i])

        return redirect("/setting.html")


def setting_upcycled(request):
    if (request.method == 'POST'):
        filepath = request.FILES.getlist('imgname')

        firebase = Firebase(config)
        storage = firebase.storage()
        for i in range(len(filepath)):
            storage.child("setting/Upcycled Product/upcycled.jpg").put(filepath[i])

        return redirect("/setting.html")

def setting_sale(request):
    if (request.method == 'POST'):
        filepath = request.FILES.getlist('imgname')

        firebase = Firebase(config)
        storage = firebase.storage()
        for i in range(len(filepath)):
            storage.child("setting/Sale Page/sale.jpg").put(filepath[i])

        return redirect("/setting.html")


def setting_trending(request):
    if (request.method == 'POST'):
        filepath = request.FILES.getlist('imgname')

        firebase = Firebase(config)
        storage = firebase.storage()
        for i in range(len(filepath)):
            storage.child("setting/Trending Page/trending.jpg").put(filepath[i])

        return redirect("/setting.html")



def stock(request):
    return render(request,'stock.html',{})