
import streamlit as st
import pandas as pd
from datetime import datetime
import math

st.set_page_config(
    page_title="FINBANK",
    page_icon="🏦",
    layout="wide"
)

# =========================
# KHỞI TẠO DỮ LIỆU
# =========================
if "balance" not in st.session_state:
    st.session_state.balance = 50000000

if "cards" not in st.session_state:
    st.session_state.cards = []

if "savings" not in st.session_state:
    st.session_state.savings = []

if "loans" not in st.session_state:
    st.session_state.loans = []

if "history" not in st.session_state:
    st.session_state.history = []

def money(number):
    return f"{number:,.0f} VNĐ"

def add_history(action, amount, note):
    st.session_state.history.append({
        "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Giao dịch": action,
        "Số tiền": money(amount),
        "Nội dung": note
    })

# =========================
# GIAO DIỆN
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #f3f6fb;
}
h1, h2, h3 {
    color: #123c69;
}
div[data-testid="stMetric"] {
    background: white;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #dce5f1;
}
</style>
""", unsafe_allow_html=True)

st.title("🏦 FINBANK")
st.caption("Ngân hàng số mô phỏng - An toàn, tiện lợi, hiện đại")

menu = st.sidebar.radio(
    "MENU",
    [
        "🏠 Trang chủ",
        "💳 Mở thẻ",
        "💰 Gửi tiết kiệm",
        "🏦 Vay vốn",
        "📊 Lịch sử giao dịch",
        "ℹ️ Giới thiệu"
    ]
)

# =========================
# TRANG CHỦ
# =========================
if menu == "🏠 Trang chủ":
    st.title("Xin chào! Chào mừng đến FINBANK")

    st.subheader("Tổng quan tài khoản")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Số dư hiện tại",
            money(st.session_state.balance)
        )

    with col2:
        total_saving = sum(
            item["Gốc"] + item["Lãi dự kiến"]
            for item in st.session_state.savings
        )
        st.metric("Tổng tiền tiết kiệm dự kiến",
                  money(total_saving))

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Số thẻ đã mở", len(st.session_state.cards))

    with col2:
        st.metric("Sổ tiết kiệm", len(st.session_state.savings))

    with col3:
        st.metric("Khoản vay mô phỏng", len(st.session_state.loans))

    st.divider()
    st.subheader("Giao dịch nhanh")

    tab1, tab2 = st.tabs(["Nạp tiền", "Rút tiền"])

    with tab1:
        amount = st.number_input(
            "Số tiền muốn nạp",
            min_value=0,
            step=100000,
            key="deposit"
        )

        if st.button("Nạp tiền", key="deposit_btn"):
            if amount > 0:
                st.session_state.balance += amount
                add_history("Nạp tiền", amount, "Nạp vào tài khoản")
                st.success("Nạp tiền mô phỏng thành công!")
                st.rerun()
            else:
                st.warning("Vui lòng nhập số tiền hợp lệ.")

    with tab2:
        amount = st.number_input(
            "Số tiền muốn rút",
            min_value=0,
            step=100000,
            key="withdraw"
        )

        if st.button("Rút tiền", key="withdraw_btn"):
            if amount <= 0:
                st.warning("Vui lòng nhập số tiền hợp lệ.")
            elif amount > st.session_state.balance:
                st.error("Số dư không đủ!")
            else:
                st.session_state.balance -= amount
                add_history("Rút tiền", amount, "Rút từ tài khoản")
                st.success("Rút tiền mô phỏng thành công!")
                st.rerun()

# =========================
# MỞ THẺ
# =========================
elif menu == "💳 Mở thẻ":
    st.title("💳 Đăng ký mở thẻ")

    with st.form("card_form"):
        name = st.text_input("Họ và tên")
        card_type = st.selectbox(
            "Loại thẻ",
            ["Thẻ ghi nợ nội địa", "Thẻ ghi nợ quốc tế", "Thẻ tín dụng mô phỏng"]
        )
        submit = st.form_submit_button("Đăng ký mở thẻ")

    if submit:
        if not name.strip():
            
            st.warning("Vui lòng nhập họ tên.")
        else:
            card = {
                "Chủ thẻ": name,
                "Loại thẻ": card_type,
                "Mã thẻ mô phỏng": f"FB{len(st.session_state.cards)+1:06d}",
                "Ngày mở": datetime.now().strftime("%d/%m/%Y")
            }

            st.session_state.cards.append(card)
            add_history("Mở thẻ", 0, card_type)
            st.success("Đăng ký thẻ mô phỏng thành công!")

    st.subheader("Danh sách thẻ")

    if st.session_state.cards:
        st.dataframe(
            pd.DataFrame(st.session_state.cards),
            use_container_width=True
        )
    else:
        st.info("Chưa có thẻ nào được đăng ký.")

# =========================
# GỬI TIẾT KIỆM
# =========================
elif menu == "💰 Gửi tiết kiệm":
    st.title("💰 Gửi tiết kiệm")

    st.write("Lãi suất giả định: 3% - 6%/năm.")

    with st.form("saving_form"):
        principal = st.number_input(
            "Số tiền gốc gửi (VNĐ)",
            min_value=0,
            step=1000000
        )

        months = st.selectbox(
            "Kỳ hạn gửi",
            [1, 3, 6, 9, 12, 18, 24]
        )

        rate = st.selectbox(
            "Lãi suất (%/năm)",
            [3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]
        )

        submit = st.form_submit_button("Xác nhận gửi tiết kiệm")

    if submit:
        if principal <= 0:
            st.warning("Vui lòng nhập số tiền hợp lệ.")
        elif principal > st.session_state.balance:
            st.error("Số dư tài khoản không đủ.")
        else:
            interest = principal * (rate / 100) * (months / 12)
            total = principal + interest

            saving = {
                "Gốc": principal,
                "Lãi suất": rate,
                "Kỳ hạn (tháng)": months,
                "Lãi dự kiến": interest,
                "Tổng nhận khi đáo hạn": total
            }

            st.session_state.savings.append(saving)
            st.session_state.balance -= principal

            add_history(
                "Gửi tiết kiệm",
                principal,
                f"Gốc {money(principal)}, lãi dự kiến {money(interest)}"
            )

            st.success("Đã tạo sổ tiết kiệm mô phỏng!")
            st.rerun()

    st.divider()
    st.subheader("Danh sách sổ tiết kiệm")

    if st.session_state.savings:
        df = pd.DataFrame(st.session_state.savings)
        st.dataframe(df, use_container_width=True)

        total_principal = sum(x["Gốc"] for x in st.session_state.savings)
        total_interest = sum(x["Lãi dự kiến"] for x in st.session_state.savings)
        total_receive = total_principal + total_interest

        c1, c2, c3 = st.columns(3)
        c1.metric("Tổng tiền gốc", money(total_principal))
        c2.metric("Tổng lãi dự kiến", money(total_interest))
        c3.metric("Tổng tiền đáo hạn", money(total_receive))
    else:
        st.info("Chưa có sổ tiết kiệm.")

# =========================
# VAY VỐN
# =========================
elif menu == "🏦 Vay vốn":
    st.title("🏦 Công cụ tính khoản vay")
    st.write("Lãi suất giả định: 6% - 12%/năm.")

    with st.form("loan_form"):
        borrower = st.text_input("Tên người vay")

        principal = st.number_input(
            "Số tiền vay (VNĐ)",
            min_value=0,
            step=1000000
        )

        months = st.selectbox(
            "Thời hạn vay (tháng)",
            [6, 12, 18, 24, 36, 48, 60]
        )

        rate = st.selectbox(
            "Lãi suất (%/năm)",
            [6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
        )

        submit = st.form_submit_button("Tính khoản vay")

    if submit:
        if not borrower.strip():
            st.warning("Vui lòng nhập tên người vay.")
        elif principal <= 0:
            st.warning("Số tiền vay phải lớn hơn 0.")
        else:
            monthly_rate = rate / 100 / 12

            if monthly_rate == 0:
                payment = principal / months
            else:
                payment = (
                    principal * monthly_rate *
                    (1 + monthly_rate) ** months
                ) / (
                    (1 + monthly_rate) ** months - 1
                )

            balance = principal
            schedule = []
            total_interest = 0
            total_principal = 0

            for month in range(1, months + 1):
                interest = balance * monthly_rate
                principal_paid = min(payment - interest, balance)
                actual_payment = principal_paid + interest
                balance = max(0, balance - principal_paid)

                total_interest += interest
                total_principal += principal_paid

                schedule.append({
                    "Tháng": month,
                    "Dư nợ đầu kỳ": round(balance + principal_paid),
                    "Tiền gốc": round(principal_paid),
                    "Tiền lãi": round(interest),
                    "Tổng phải trả": round(actual_payment),
                    "Dư nợ cuối kỳ": round(balance)
                })

            loan = {
                "Người vay": borrower,
                "Tiền vay": principal,
                "Lãi suất": rate,
                "Kỳ hạn": months,
                "Trả hàng tháng": payment,
                "Tổng gốc": total_principal,
                "Tổng lãi": total_interest,
                "Tổng thanh toán": total_principal + total_interest,
                "Bảng trả nợ": schedule
            }

            st.session_state.loans.append(loan)

            add_history(
                "Tính khoản vay",
                principal,
                f"Khoản vay mô phỏng của {borrower}"
            )

            st.success("Đã tính toán khoản vay mô phỏng!")

    st.divider()
    st.subheader("Danh sách khoản vay đã tính")

    if st.session_state.loans:
        for index, loan in enumerate(st.session_state.loans):
            with st.expander(
                f"Khoản vay {index + 1} - {loan['Người vay']}"
            ):
                c1, c2 = st.columns(2)

                c1.metric("Số tiền gốc", money(loan["Tiền vay"]))
                c2.metric("Lãi suất năm", f"{loan['Lãi suất']}%")

                c1.metric(
                    "Tiền trả mỗi tháng",
                    money(loan["Trả hàng tháng"])
                )

                c2.metric(
                    "Tổng tiền lãi",
                    money(loan["Tổng lãi"])
                )

                c1.metric(
                    "Tổng tiền gốc trả",
                    money(loan["Tổng gốc"])
                )

                c2.metric(
                    "Tổng tiền phải trả",
                    money(loan["Tổng thanh toán"])
                )

                st.write("### Bảng lịch trả nợ")
                df = pd.DataFrame(loan["Bảng trả nợ"])
                st.dataframe(df, use_container_width=True)

                csv = df.to_csv(index=False).encode("utf-8-sig")

                st.download_button(
                    "Tải bảng trả nợ CSV",
                    data=csv,
                    file_name=f"lich_tra_no_{index+1}.csv",
                    mime="text/csv",
                    key=f"download_{index}"
                )
    else:
        st.info("Chưa có khoản vay nào được tính.")

# =========================
# LỊCH SỬ GIAO DỊCH
# =========================
elif menu == "📊 Lịch sử giao dịch":
    st.title("📊 Lịch sử giao dịch")

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            "📥 Tải lịch sử giao dịch",
            data=csv,
            file_name="lich_su_finbank.csv",
            mime="text/csv"
        )
    else:
        st.info("Chưa có giao dịch nào.")

# =========================
# GIỚI THIỆU
# =========================
elif menu == "ℹ️ Giới thiệu":
    st.title("ℹ️ Về FINBANK")

    st.write("""
    **FINBANK** là ứng dụng ngân hàng số mô phỏng được xây dựng
    nhằm phục vụ mục đích học tập và thuyết trình.

    Các chức năng chính:

    - Quản lý số dư tài khoản mô phỏng.
    - Đăng ký thẻ ngân hàng mô phỏng.
    - Gửi tiết kiệm và tính tiền lãi.
    - Tính khoản vay và lịch trả nợ.
    - Theo dõi lịch sử giao dịch.
    - Xuất dữ liệu ra file CSV.

    Lưu ý: Đây không phải ngân hàng thật.
    Không có giao dịch tiền thật, phát hành thẻ thật
    hoặc giải ngân khoản vay thật.
    """)

st.sidebar.divider()
st.sidebar.caption("FINBANK | Phiên bản học tập 2.0")
st.sidebar.caption("Dữ liệu mô phỏng, có thể mất khi phiên chạy kết thúc.")



            
