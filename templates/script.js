  function update_list()
  {
     url = "http://fhem-vm.aljam.de/list" //achtung Access-Control-Allow-Origin: setzen, muss eine rihtige url sein damit local debugt werden kann
     //url = "list"
     fetch( url )
        .then( response => {
           if( !response.ok )
              throw new Error( "fetch failed in update_u_eingang() :" + url  ) ;
           return response.json() ;
        } )
        .then( json => {
              document.querySelector("#id3011v").textContent = json.id3011.value;
              document.querySelector("#id3011n").textContent = json.id3011.name;
              document.querySelector("#id3011u").textContent = json.id3011.unit;
              document.querySelector("#id3022v").textContent = json.id3022.value;
              document.querySelector("#id3022n").textContent = json.id3022.name;
              document.querySelector("#id3022u").textContent = json.id3022.unit;
              //console.log(json.id3011.value);

              element = document.getElementById("button1") 
              element.textContent = json.id3011.value;
              console.log('Running ... ');
           } 
        )
        .catch((error) => {
           console.error('Error:', error);
        });
  }
  update_list() ;


  function update_u_eingang()
  {
     fetch( "/u_eingang" )
        .then( response => {
           if( !response.ok )
              throw new Error( "fetch failed" ) ;

           return response.json() ;
        } )
        .then( json => document.querySelector("#u_eingang").textContent = json.u_eingang )
        .catch( error => alert(error) ) ;
  }
  //update_u_eingang() ;



  function get_value_by_id(id)
  {
     //fetch( "/value_by_id?id=" + id.toString())
     //url = "/value_by_id"
     //fetch(url, params = {id:3005})
     //url = "/value_by_id"
     var url = new URL("http://fhem.aljam.de:5000/value_by_id"), params = {id:3000}
     Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
     fetch(url)
        .then( response => 
        {
           if( !response.ok )
              throw new Error( "fetch failed in get_value_by_id() : " + url ) ;

           return response.json() ;
        } )
        .then( json => document.querySelector("#id_" + id.toString()).textContent = json.value_by_id )
        .catch( error => alert(error) ) ;
  }


  function get_value_by_id1(id)
  {
     //fetch( "/value_by_id?id=" + id.toString())


     const url = '/value_by_id';

     let data = {
        id: '3000'
     }

     var request = new Request(url, {
        method: 'POST',
        body: data,
        headers: new Headers()
     });

     fetch(url)
        .then( response => 
        {
           if( !response.ok )
              throw new Error( "fetch failed in get_value_by_id() : " + url ) ;

           return response.json() ;
        } )
        .then( json => document.querySelector("#id_" + id.toString()).textContent = json.value_by_id )
        .catch( error => alert(error) ) ;
  }


  function update_all()
  {
     get_value_by_id(3000);
  }
  //update_all();



  setInterval( update_list, 5000 ) ;
  //setInterval( update_u_eingang, 3000 ) ;
  //setInterval( update_all, 3000 ) ;

