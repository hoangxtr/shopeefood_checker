import json
from fastapi import FastAPI
from check_shopee_order import  ShopeeFoodDataTracking
from datetime import datetime
app = FastAPI()
shopee_checker = ShopeeFoodDataTracking()

@app.get("/check_order")
async def check_order():
    try:
        with open('histories.json', 'r') as f:
            data = json.load(f)
        if data['last_update_time'] != datetime.now().date().strftime("%Y-%m-%d"):
            histories = {
                "dish_reports": [],
                "dish_sum_total": 0,
                "value_sum_total": "",
                "last_update_time": datetime.now().date().strftime("%Y-%m-%d")
            }
            with open('histories.json', 'w') as f:
                json.dump(histories, f, indent=4)
        
        ret = shopee_checker.process()    
        return ret
    except Exception as e:
        from fastapi.responses import JSONResponse
        return JSONResponse(content={"message": f"An error occurred: {e}"}, status_code=403)

# def foo():
#     with open('histories.json', 'r') as f:
#         data = json.load(f)
#     if data['last_update_time'] != datetime.now().date().strftime("%Y-%m-%d"):
#         histories = {
#             "dish_reports": [],
#             "dish_sum_total": 0,
#             "value_sum_total": "",
#             "last_update_time": datetime.now().date().strftime("%Y-%m-%d")
#         }
#         with open('histories.json', 'w') as f:
#             json.dump(histories, f, indent=4)
    
#     ret = shopee_checker.process()    
#     return ret

# print(foo())