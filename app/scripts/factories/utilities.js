angularApp.factory('Util', ["$window",function($window) {
  var util = {
    FormatLog:function(Log){
      var result = "";
      if(Log.stream){
        result = Log.stream;
      }
      if(Log.status && Log.progressDetail && Log.id){
        var percent = "100%";
        if(Log.progressDetail.current){
          percent = parseInt(Log.progressDetail.current*100 / Log.progressDetail.total)+"%";
        }
        result = Log.status+" "+Log.id+" "+percent;
      }
      if(Log.status &&　Log.progressDetail && Log.progress){
        var percent = "100%";
        if(Log.progressDetail.current){
          percent = parseInt(Log.progressDetail.current*100 / Log.progressDetail.total)+"%";
        }
        result = Log.status+" "+percent+" "+Log.progress;
      }
      return result;
    }
  };
  return util;
}]);
