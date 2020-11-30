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
        formatMonth= today.strftime("%Y-%m") # Get the current month
        
        cur.execute("SELECT AVG(soil), AVG(temperature), AVG(air), AVG(light)  FROM gui_sensorrecord WHERE plant_id = ? AND create_time LIKE '?%' ",(plantId,formatMonth))
        monthlySensorRecord = cur.fetchall()
        averageSoil = monthlySensorRecord[0]
        averageTemp = monthlysensorRecord[1]
        averageAir = monthlysensorRecord[2]
        averageLight = monthlysensorRecord[3]

        cur.execute("INSERT INTO gui_dailysensorrecord(soil,temperature,air,light,create_time,plant_id) VALUE(?,?,?,?,?,?)",
                (averageSoil, averageTemp, averageAir, averageLight, formatMonth, plantId)
    except mariadb.Error as e:
        print(e)
