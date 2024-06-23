import json

class Variables:
    def __init__(self):
        self._variables = {}
        self._observers = []
        self.load_variables()


    # Observer 등록
    def register_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)


    # Observer들의 update() 실행
    def notify_observers(self, *args):
        for observer in self._observers:
            observer.update(*args)


    # 환경값 저장
    def set_variable(self, key, value):
        self._variables[key] = value
        self.notify_observers(key, value)


    # 환경값 가져오기
    def get_variable(self, key):
        return self._variables.get(key, None) # 해당 key가 없으면 None을 반환    


    # config.json에서 저장된 값 가져오기
    def load_variables(self):
        try:
            with open('config.json', 'r') as file:
                self._variables = json.load(file)
        except FileNotFoundError:
            print("config.json 파일이 없습니다. 기본 값을 사용합니다.")
        except json.JSONDecodeError:
            print("config.json 파일의 형식이 잘못되었습니다. 기본 값을 사용합니다.")


    # json에 저장된 환경값 저장하기
    def save_variables(self):
        with open('config.json', 'w') as file:
            json.dump(self._variables, file)