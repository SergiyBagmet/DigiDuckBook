from datetime import date, timedelta

class CalculateDate:
    
    @staticmethod
    def days_to_birthday(birthday: date) -> int:
        today = date.today()
        try:
            bday = birthday.replace(year=today.year)  # дата др в этом году
            if (today > bday):  # если др уже прошло берем дату следующего(в следующем году)
                bday = bday.replace(year=today.year + 1)
            return (bday - today).days
        except ValueError:  # исключение для високосной дати 1го дня уууу-02-29
            if birthday.month == 2 and birthday.day == 29 : 
                return CalculateDate.days_to_birthday(birthday.replace(day=28)) + 1
            else: ValueError
            
    @staticmethod
    def find_obj_in_day_interval(data: dict[object, date], delta_days: int) -> list[object]:
        current_date = date.today()
        time_delta = timedelta(days=delta_days)
        end_date = current_date + time_delta
        list_obj = []
        for obj, birthday in data.items():
            birthday = birthday.replace(year=current_date.year) 
            if (current_date <= birthday <=end_date):
                list_obj.append(obj)
        return list_obj