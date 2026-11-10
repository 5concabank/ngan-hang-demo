
import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

st.set_page_config(
    page_title="FINBANK",
    page_icon="🏦",
    layout="wide"
)

# ===== KHOI TAO DU LIEU =====
if "balance" not in st.session_state:
    st.session_state.balance = 50000000

for key in ["cards", "savings", "loans", "history"]:
    if key not in st.session_state:
        st.session_state[key] = []

def money(x):
    return f"{x:,.0f} VND"

def record(action, amount, note):
    st.session_state.history.insert(0, {
        "Ma giao dich": str(uuid.uuid4())[:8].upper(),
        "Thoi gian": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Dich vu": action,
        "So tien": money(amount),
        "Noi dung": note
    })

# ===== GIAO DIEN =====
st.markdown("""
<style>
.stApp {
    background-color: #f2f6fc;
}
section[data-testid="stSidebar"] {
    background-color: #12345a;
}
section[data-testid="stSidebar"] * {
    color: white;
}
div[data-testid="stMetric"] {
    background: white;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #dce5f0;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🏦 FINBANK")
st.sidebar.caption("DIGITAL BANKING")
st.sidebar.write("Ngân hàng số mô phỏng")

menu = st.sidebar.radio(
    "DỊCH VỤ",
    [
        "🏠 Trang chủ",
        "💳 Mở thẻ",
        "💰 Gửi tiết kiệm",
        "🏦 Vay vốn",
        "📋 Lịch sử",
        "ℹ️ Giới thiệu"
    ]
)

# ===== TRANG CHU =====
if menu == "🏠 Trang chủ":

    st.title("🏦 FINBANK")
    st.subheader("NGÂN HÀNG SỐ THÔNG MINH")

    st.success("Chào mừng bạn đến với FINBANK!")

    c1, c2, c3 = st.columns(3)

    c1.metric("Số dư mô phỏng", money(st.session_state.balance))
    c2.metric("Số thẻ", len(st.session_state.cards))
    c3.metric("Sổ tiết kiệm", len(st.session_state.savings))

    st.divider()

    st.subheader("Dịch vụ của chúng tôi")

    a, b = st.columns(2)

    with a:
        st.info("💳 MỞ THẺ NGÂN HÀNG")
        st.write("Đăng ký thẻ ghi nợ và thẻ tín dụng mô phỏng.")

        st.info("💰 GỬI TIẾT KIỆM")
        st.write("Lựa chọn kỳ hạn và tính tiền lãi.")

    with b:
        st.info("🏦 VAY VỐN")
        st.write("Tính toán khoản vay và trả góp.")

        st.info("📋 LỊCH SỬ")
        st.write("Theo dõi hoạt động mô phỏng.")

# ===== MO THE =====
elif menu == "💳 Mở thẻ":

    st.title("💳 ĐĂNG KÝ MỞ THẺ")

    with st.form("card"):

        name = st.text_input("Họ và tên")

        card_type = st.selectbox(
            "Loại thẻ",
            ["Thẻ ghi nợ nội địa",
             "Thẻ ghi nợ quốc tế",
             "Thẻ tín dụng mô phỏng"]
        )

        card_name = st.text_input("Tên hiển thị trên thẻ")

        submit = st.form_submit_button("ĐĂNG KÝ")

    if submit:

        if not name.strip() or not card_name.strip():
            st.error("Vui lòng nhập đầy đủ thông tin.")

        else:
            st.session_state.cards.append({
                "Mã đăng ký": str(uuid.uuid4())[:8].upper(),
                "Chủ thẻ": name,
                "Loại thẻ": card_type,
                "Tên trên thẻ": card_name,
                "Ngày đăng ký": datetime.now().strftime("%d/%m/%Y")
            })

            record("Mở thẻ", 0, card_type)

            st.success("Đăng ký thẻ mô phỏng thành công!")

    if st.session_state.cards:
        st.subheader("Danh sách thẻ")
        st.dataframe(
            pd.DataFrame(st.session_state.cards),
            use_container_width=True
        )

# ===== GUI TIET KIEM =====
elif menu == "💰 Gửi tiết kiệm":

    st.title("💰 GỬI TIẾT KIỆM")

    with st.form("saving"):

        amount = st.number_input(
            "Số tiền gửi (VNĐ)",
            min_value=100000,
            value=10000000,
            step=1000000
        )

        months = st.selectbox(
            "Kỳ hạn",
            [1, 3, 6, 9, 12, 18, 24]
        )

        rate = st.selectbox(
            "Lãi suất năm giả định (%)",
            [3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]
        )

        submit = st.form_submit_button("XÁC NHẬN GỬI")

    if submit:

        if amount > st.session_state.balance:
            st.error("Số dư mô phỏng không đủ.")

        else:
            interest = amount * rate / 100 * months / 12
            total = amount + interest

            st.session_state.balance -= amount

            st.session_state.savings.append({
                "Mã sổ": str(uuid.uuid4())[:8].upper(),
                "Tiền gửi": amount,
                "Kỳ hạn": months,
                "Lãi suất": rate,
                "Tiền lãi": interest,
                "Tổng nhận": total
            })

            record("Gửi tiết kiệm", amount, f"{months} tháng")

            st.success("Tạo sổ tiết kiệm mô phỏng thành công!")

            st.metric("Tiền lãi dự kiến", money(interest))
            st.metric("Tổng tiền cuối kỳ", money(total))

    if st.session_state.savings:
        st.subheader("Danh sách tiết kiệm")
        st.dataframe(
            pd.DataFrame(st.session_state.savings),
            use_container_width=True
        )

# ===== VAY VON =====
elif menu == "🏦 Vay vốn":

    st.title("🏦 ĐĂNG KÝ VAY VỐN")

    st.warning("Chỉ là công cụ tính toán vay vốn mô phỏng.")

    with st.form("loan"):

        name = st.text_input("Họ và tên")

        amount = st.number_input(
            "Số tiền muốn vay (VNĐ)",
            min_value=1000000,
            value=50000000,
            step=1000000
        )

        months = st.selectbox(
            "Thời hạn vay (tháng)",
            [6, 12, 18, 24, 36, 48, 60]
        )

        rate = st.selectbox(
            "Lãi suất năm giả định (%)",
            [6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
        )

        submit = st.form_submit_button("TÍNH KHOẢN VAY")

    if submit:

        if not name.strip():
            st.error("Vui lòng nhập họ tên.")

        else:
            r = rate / 100 / 12

            if r == 0:
                payment = amount / months
            else:
                payment = (
                    amount * r * (1 + r) ** months
                    / ((1 + r) ** months - 1)
                )

            total = payment * months
            interest = total - amount

            st.session_state.loans.append({
                "Mã yêu cầu": str(uuid.uuid4())[:8].upper(),
                "Người đăng ký": name,
                "Tiền vay": amount,
                "Thời hạn": months,
                "Lãi suất": rate,
                "Trả mỗi tháng": payment,
                "Tổng lãi": interest,
                "Trạng thái": "Mô phỏng - chưa phê duyệt"
            })

            record("Tính khoản vay", amount, f"{months} tháng")

            st.success("Đã tính khoản vay mô phỏng!")

            st.metric("Trả mỗi tháng", money(payment))
            st.metric("Tổng tiền lãi", money(interest))
            st.metric("Tổng thanh toán", money(total))

    if st.session_state.loans:
        st.subheader("Danh sách yêu cầu vay")
        st.dataframe(
            pd.DataFrame(st.session_state.loans),
            use_container_width=True
        )

# ===== LICH SU =====
elif menu == "📋 Lịch sử":

    st.title("📋 LỊCH SỬ GIAO DỊCH")

    if st.session_state.history:

        st.dataframe(
            pd.DataFrame(st.session_state.history),
            use_container_width=True
        )

        csv = pd.DataFrame(
            st.session_state.history
        ).to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            "TẢI LỊCH SỬ",
            csv,
            "lich_su_FINBANK.csv",
            "text/csv"
        )

    else:
        st.info("Chưa có giao dịch nào.")

# ===== GIOI THIEU =====
elif menu == "ℹ️ Giới thiệu":

    st.title("ℹ️ VỀ FINBANK")

    st.subheader("Ngân hàng số thông minh")

    st.write("""
    FINBANK là ứng dụng ngân hàng mô phỏng được xây dựng
    bằng Python và Streamlit nhằm phục vụ mục đích học tập.

    Các chức năng chính:

    - Đăng ký mở thẻ ngân hàng.
    - Gửi tiết kiệm và tính lãi.
    - Tính toán khoản vay vốn.
    - Theo dõi lịch sử giao dịch.

    FINBANK không phải tổ chức tín dụng và không thực hiện
    giao dịch tài chính thật.
    """)

    st.success("FINBANK - Kết nối tương lai!")
    st.caption("Phiên bản 1.0 - Dự án học tập")
