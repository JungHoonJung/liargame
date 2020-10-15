# liargame

헤로쿠(heroku)는 서버를 제공하는 인터넷 호스팅 기업인 듯 하다.

사용법은

`Procfile` 이라는 파일내에
```<process>:<command>```
형식으로 적으면 된다.

단, 외부 라이브러리 같은 경우에는 `requirements.txt`에 적어주어야 한다.

깃헙으로도 배포할 수 있어서 관리나 배포가 aws lambda보다 훨씬 쉬워보인다.
이거나 써야지
