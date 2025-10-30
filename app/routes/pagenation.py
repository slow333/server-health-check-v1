from flask import request
from ..extensions import db

def pagenation(obj):
    page = request.args.get("page", 1, type=int)
    per_page = 5
    offset = (page - 1) * per_page

    query_result = (
       db.session.query(obj)
         .order_by(obj.id.desc())
         .limit(per_page)
         .offset(offset)
         .all()
    )

    total = db.session.query(obj).count()

    # 페이지네이션: 현재 페이지 기준으로 최대 5개 페이지만 표시
    total_pages = (total // per_page) + (1 if total % per_page else 0)
    page_len = len(query_result)

    start_page = max(1, page - 2)
    end_page = min(total_pages, start_page + (per_page -1))
    if end_page - start_page < (per_page -1):
        start_page = max(1, end_page - (per_page -1))

    pagination_data = {
        'query_result': query_result,
        'page': page,
        'per_page': per_page,        
        'total_pages': total_pages,
        'page_len': page_len,
        'start_page': start_page,
        'end_page': end_page
    }
    return pagination_data