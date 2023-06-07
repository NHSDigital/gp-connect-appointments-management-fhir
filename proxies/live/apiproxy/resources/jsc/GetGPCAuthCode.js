function json_tryparse(raw) {
    try {
        return JSON.parse(raw);
    }
    catch (e) {
        return raw;
    }
  }

  var respContent=context.getVariable('GPCPFSAuthResponse.content');
  const respObject=JSON.parse(respContent);
  context.setVariable("request.header.Authorization", respObject["access_token"]);
