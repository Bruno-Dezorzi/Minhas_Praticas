import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      ),
      home: Container(
        color: Colors.white,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Stack(
              alignment: AlignmentDirectional.center,
              children: [
                Container(color: Colors.amber, width: 100, height: 100),
                Container(color: Colors.red, width: 50, height: 50),
              ],
            ),
            Stack(
              alignment: AlignmentDirectional.center,
              children: [
                Container(color: Colors.blue, width: 100, height: 100),
                Container(color: Colors.green, width: 50, height: 50),
              ],
            ),
            Row(
             mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                Container(color: Colors.blue, width: 50, height: 50),
                Container(color: const Color.fromARGB(255, 255, 0, 0), width: 50, height: 50),
                Container(color: Colors.green, width: 50, height: 50),
              ],
            ),
            Container(
              color: Colors.amber,
              height: 30,
              width: 300,
              child: Text(
                'Diamante amarelo',
                style: TextStyle(
                  color: Colors.black,
                  fontSize: 28,
                  ),
                  textAlign: TextAlign.center,
                ),
            ),
            ElevatedButton(
              onPressed: (){print('Você apertou o botão');},
               child: Text("Aperte o Botão!"),
               ),
            
          ],
        ),
      ),
    );
  }
}
