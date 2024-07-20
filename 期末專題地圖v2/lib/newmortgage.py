import json
def calculate_loan_payments(principal, years, annual_rate=2.18):
    if annual_rate < 1: annual_rate*=100
    # 將年利率轉換為月利率
    principal *= 10000
    monthly_rate = annual_rate / 100 / 12
    # 總月數
    total_months = years * 12

    # 計算每月還款金額（EMI）
    emi = (principal * monthly_rate) / (1 - (1 + monthly_rate) ** -total_months)

    # 計算總還款額和總利息
    total_repayment = emi * total_months
    total_interest = total_repayment - principal
    result = {}
    result["monthly_payment"] = int(emi)
    result["total_repayment"] = int(total_repayment)
    result["total_interest"] = int(total_interest)
    
    result = json.dumps(result)
    # result.append({
    #     "monthly_payment": int(emi),
    #     "total_repayment": int(total_repayment), 
    #     "total_interest": int(total_interest)})
    return result

def main():
    # 讓使用者輸入貸款總額和還款年限
    principal = float(input("請輸入貸款總額萬（例如 1000）："))
    years = int(input("請輸入還款年限（例如 20）："))

    # 計算結果
    answer = calculate_loan_payments(principal, years)
    answer = json.loads(answer)
    # print(type(answer))
    # # 顯示結果
    print(f"每月還款金額（EMI）：{answer['monthly_payment']:.2f} 元")
    print(f"總還款額：{answer['total_repayment']:.2f} 元")
    print(f"總利息：{answer['total_interest']:.2f} 元")

if __name__ == "__main__":
    main()
