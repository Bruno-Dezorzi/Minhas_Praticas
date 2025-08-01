const express = require('express')
const app = express()
const port = 3000

app.get('/',(req,res) =>{
    res.send("Ola!!!!!!")
})

app.listen(port, () =>{
    console.log(`Executando a porta: ${port}`)
})