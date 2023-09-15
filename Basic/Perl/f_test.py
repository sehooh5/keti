student_id = """2013105296
2012124644
2013123412
2014107400
2012110499
2013100102
2011139940
2014131487"""
major_id = {'10':'경영학과', '11':'사회학과', '12':'국문학과', '13':'물리학과'}

def count_id(student_id):

    s_ids = student_id.split()
    cnt_y = {}
    cnt_m = {}

    for s_id in s_ids:
        y = s_id[2]+s_id[3]
        m_id = s_id[4]+s_id[5]
        m = major_id[m_id]

        if y in cnt_y:
            cnt_y[y] += 1
        else:
            cnt_y[y] = 1

        if m in cnt_m:
            cnt_m[m] += 1
        else:
            cnt_m[m] = 1

    print("기수별 학생 수:", dict(sorted(cnt_y.items())))
    print("학과별 학생 수:", cnt_m)

count_id(student_id)



