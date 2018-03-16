import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css',
    '../../../assets/bootstrap/css/bootstrap.min.css',
    '../../../assets/font-awesome/css/font-awesome.min.css',
    '../../../assets/css/form-elements.css',
    '../../../assets/css/style.css']
})
export class SignUpComponent implements OnInit {

  constructor() { }

  ngAfterViewInit() {
    var dynamicScripts = ["../../../assets/js/jquery-1.11.1.min.js","../../../assets/bootstrap/js/bootstrap.min.js","../../../assets/js/jquery.backstretch.min.js","../../../assets/js/scripts.js"];

    for (var i = 0; i < dynamicScripts .length; i++) {
        let node = document.createElement('script');
        node.src = dynamicScripts [i];
        node.type = 'text/javascript';
        node.async = false;
        node.charset = 'utf-8';
        document.getElementsByTagName('head')[0].appendChild(node);
    }
  }
  
  ngOnInit() {
  }

  onSubmit(data) {
    console.log("Entered Email id : " + data.email+ ' '+ data.password1);
  }
}
