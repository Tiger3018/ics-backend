package main

import (
	"fmt"
	"log"
	"os"
	"os/exec"
	"strings"

	"github.com/gin-gonic/gin"
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

func parseStaticICS(b1 bool) gin.HandlerFunc {
	return func(c *gin.Context) {
		var prefer preferenceStudent
		fileName := c.Param("id")
		checkInput := strings.Split(fileName, ".")
		if c.ShouldBind(&prefer) == nil {
			log.Println("prefer list:", prefer)
		} else {
			c.String(400, "Your paramater may be incorrect...")
			return
		}
		if len(checkInput) == 2 && checkInput[1] == "ics" && len(strings.Split(checkInput[0], "/")) == 1 {
			if b1 != false {
				out, err := exec.Command("python3", "pytask/single.py", checkInput[0]).CombinedOutput()
				if err != nil {
					fmt.Printf("%s\n", out)
					log.Println("when exec(), some error happened...", err)
				} else {
					fmt.Printf("%s\n", out)
				}
			}
			c.File("./ics/" + fileName)
		} else {
			c.String(400, "Your input may be insecure...")
			return
		}
	}
}

func main() {
	gin.SetMode(gin.ReleaseMode)
	router := gin.Default()
	router.GET("/student-cron/:id", parseStaticICS(false))
	router.GET("/student/:id", parseStaticICS(true))
	log.Print("Server listening...\n")
	log.Fatal(router.Run("0.0.0.0:" + os.Getenv("PORT")))
}
