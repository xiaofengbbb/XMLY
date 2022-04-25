package main

import (
	"database/sql"
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"os"
	"smokeTest/database"
	"strconv"
)

type Music []struct {
	MusicURL   string `json:"musicUrl"`
	MusicIndex int    `json:"musicIndex"`
}

func toJson(albumId string) Music {
	// jsonFile, err := os.Open("result-json-" + albumId + ".txt")
	jsonFile, err := os.Open("F://python//WorkPlace//ximalaya//result-json-" + albumId + ".txt")
	if err != nil {
		fmt.Println("error opening json file,err:", err)
		return nil
	}
	defer jsonFile.Close()

	jsonData, err := ioutil.ReadAll(jsonFile)
	if err != nil {
		fmt.Println("error reading json file")
		return nil
	}
	var music Music
	json.Unmarshal(jsonData, &music)
	return music
}

func toDB() *sql.DB {
	dialect := fmt.Sprintf("%s:%s@tcp(%s:%d)/%s?charset=utf8&parseTime=True&loc=Local",
		"root",
		"123456",
		"127.0.0.1",
		3306,
		"xmly",
	)
	db, err := database.New("mysql", dialect)
	if err != nil {
		fmt.Println("MySQL Database connection error", "DBName", "test", "error", err)
		os.Exit(1)
	}
	fmt.Printf("\n[~]MySQL Database is connected successfully.\n")
	return db.DB

}

func createTable(db *sql.DB, albumId string) {

	sql := "DROP TABLE IF EXISTS xmly" + albumId + ";"
	_, err := db.Exec(sql)
	if err != nil {
		fmt.Println("delete table error:", err)
	}
	fmt.Println("[~]drop table if exist success!")
	sql = "CREATE TABLE xmly" + albumId + " (UrlIndex INT(11) PRIMARY KEY,URL VARCHAR(200),PATH VARCHAR(200));"
	_, err = db.Exec(sql)
	if err != nil {
		fmt.Println("create table error:", err)
	}
	fmt.Println("[~]create table success!")

}

func main() {
	//配置参数
	var configVersion = flag.String("albumId", "3555870", "select albumId")
	flag.Parse()
	//连接数据库
	db := toDB()
	defer db.Close()
	//创建albumId表
	createTable(db, *configVersion)
	//由json数据转化为struct切片
	music := toJson(*configVersion)
	//存储到数据库
	for i := 0; i < len(music); i++ {
		sql := "INSERT INTO xmly" + *configVersion + " VALUES (?,?,?)"
		path := "F://python//WorkPlace//ximalaya//" + strconv.Itoa(music[i].MusicIndex) + ".m4a"
		_, err := db.Query(sql, music[i].MusicIndex, music[i].MusicURL, path)
		if err != nil {
			fmt.Println("插入数据失败")
		}
	}
	fmt.Println("[~]insert message success!")
}
