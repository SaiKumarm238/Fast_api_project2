from typing import List, Optional
from fastapi import APIRouter, Cookie,  Form, Header
from fastapi.responses import Response, HTMLResponse, PlainTextResponse

router = APIRouter(
    prefix='/product',
    tags=['Product']
)

products = ["watch", "camera", "phone"]

#form
@router.post('/new')
def create_product(name:str= Form(...)):
    products.append(name)
    return products

#How to set Cookie and Response
@router.get('/all')
def get_all_productes():
    # return products
    data = " ".join(products)
    response = Response(content=data, media_type="text/plane")
    response.set_cookie(key="test_cookie", value="test_coolie_value")
    return response

#how to set Headers and Response and get cookie
@router.get('/withheader')
def get_product_head(
    response: Response,
    custome_header:Optional[List[str]] = Header(None),
    test_cookie: Optional[str] =Cookie(None)
    ):
    if custome_header:
        response.headers['custom_response_header'] = ", ".join(custome_header)
    return {
        'data':products,
        'custome_header': custome_header,
        'my_cookie':test_cookie
    }


#Diffrent type of Resonses according to the content type plne or HTML
@router.get('/{id}', responses={
    200:{
        "content":{
            "text/html":{
                "example":"<div>Product</div>"
            }
        },
        "descripition":"Return the Html for an object"
    },
    404:{
        "content":{
            "text/plane":{
                "example":"Product not available"
            }
        },
        "descripition":"A cleartext error message"
    }
})
def get_product(id:int):
    if id > len(products):
        out = "Product not avaliable"
        return PlainTextResponse(status_code=404, content=out, media_type="text/plane")
    else:
        product = products[id]
        out=f"""
        <head>
            <style>
            .product {{
                width: 500px;
                height: 30px;
                border:2px inset green;
                background-color: lightblue;
                text-align: center;
            }}
            </style>
        </head>
        <div class="product">{product}</div>    
        """
        return HTMLResponse(content=out, media_type='text/html')