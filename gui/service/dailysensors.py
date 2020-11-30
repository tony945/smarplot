import mariadb
from datetime import date

if __name__ == '__main__':
    
    conn = mariadb.connect(
        user="tonychen",
        password="killer945",
        host="localhost",
        database="plant")
    cur = conn.cursor()

    try:
        cur.execute("SELECT pid FROM gui_plant WHERE active = ?",(1,))
        plantIds = cur.fetchall()
        plantId = plant_ids[0][0]
        today = date.today()
        formatToday= today.strftime("%Y-%m-%d")
        
        cur.execute("SELECT AVG(soil), AVG(temperature), AVG(air), AVG(light)  FROM gui_sensorrecord WHERE plant_id = ? AND create_time LIKE '?%' ",(plantId,formatToday))
        dailySensorRecord = cur.fetchall()
        averageSoil = dailySensorRecord[0]
        averageTemp = dailySensorRecord[1]
        averageAir = dailySensorRecord[2]
        averageLight = dailySensorRecord[3]

        cur.execute("INSERT INTO gui_dailysensorrecord(soil,temperature,air,light,create_time,plant_id) VALUE(?,?,?,?,?,?)",
                (averageSoil, averageTemp, averageAir, averageLight, formatToday, plantId)
    except mariadb.Error as e:
        print(e)