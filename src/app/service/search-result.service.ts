import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { of } from 'rxjs/observable/of';
import { tap } from 'rxjs/operators';
import { Paper } from '../../utils/Paper';
import { Server } from '../../utils/Server';
import { Subject } from 'rxjs/Subject';

@Injectable()
export class SearchResultService {
  searchKey:string;
  data:any;
  private subject = new Subject<any>();
  
  constructor(private http: HttpClient) { }

  getValue(): Observable<any> {
    return this.subject.asObservable();
  }

  setPaper(searchKey:string):  void{
    console.log("SET PAPER "+searchKey);
    this.searchKey=searchKey;
    if (localStorage.getItem('searchResult') != null) {
      //console.log('removing ls item');
      localStorage.removeItem('searchResult');
    }
    this.subject.next({ value: true });
  }
  
  getPapers():Observable<Paper[]>{
    console.log('get paper');
    let searchResult=localStorage.getItem('searchResult');
    if ( searchResult!= null) {
      var list = JSON.parse(searchResult);
     
      return of(list);
    }

    console.log('getting result from server\n');
    return this.http.get<Paper[]>(Server.API_ENDPOINT+'search/'+this.searchKey)
    .pipe(
      tap(response => localStorage.setItem("searchResult", JSON.stringify(response)))
    );
      //return of([]);
  }

  setAdvancedSearchPaper(data:any){
    this.data=data;
    if (localStorage.getItem('advancedSearchResult') != null) {
      localStorage.removeItem('advancedSearchResult');
      
      console.log(localStorage.getItem('advancedSearchResult'));
    }
    this.subject.next({ value: true });
  }

  getAdvancedSearchPaper():Observable<Paper[]>{
    debugger;
    let advancedSearchResult=localStorage.getItem('advancedSearchResult');
    if ( advancedSearchResult!= null) {
      var list = JSON.parse(advancedSearchResult);
      return of(list);
    }
    return this.http.get<Paper[]>(Server.API_ENDPOINT+'search/'+this.data)
    .pipe(
      tap(response => localStorage.setItem('advancedSearchResult', JSON.stringify(response)))
    );
  }
}