package main

import (
	"github.com/gin-gonic/gin"
	"log"
	"strconv"
	// "net/http"
	// "regexp"
)

type preferenceBase struct {
	Type string `form:"type"`
}

type preferenceStudent struct {
	preferenceBase
	Alert     bool `form:"alert"`
	AlertTime int  `form:"alerttime"`
}

func main() {
	gin.SetMode(gin.ReleaseMode)
	router := gin.Default()
	router.GET("/student/:id", func(c *gin.Context) {
		var prefer preferenceStudent
		if c.ShouldBind(&prefer) == nil {
			log.Println(prefer)
		} else {
			c.String(400, "Your paramater may be incorrect...")
			return
		}
		_, err := strconv.Atoi(c.Param("id"))
		if err == nil {
			c.File("./ics/" + c.Param("id") + ".ics")
		} else {
			// c.String(400, "Your request is not a student number:"+c.Param("id")+"\n")
			log.Println(err)
			return
		}
	})
	log.Fatal(router.Run("0.0.0.0:8080"))
}
