import express from "express";

const app = express();


const livros = [
    {
        id:1,
        titulo: "O Senhor dos Anéis"
    },
    {
        id:2,
        titulo: "O Hobbit"
    }
]

app.get("/",(req,res) =>{
    res.status(200);
    res.json(livros)
});

app.get("/livros",(req,res) =>{
    res.status(200).send(livros);
});

app.get("/autor",(req,res) =>{
    res.status(200).send("Entrei na rota autor");
});

app.post("/livros", (req,res) =>{
    livros.push(req.body)
});



export default app;