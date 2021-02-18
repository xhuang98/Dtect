import { extendObservable } from 'mobx';

class UserStore {

    constructor() {
        extendObservable(this, {
            loading: true,
            isLoggedIn: false,
            username: ''
        })
    }
  
}

// new instance
export default new UserStore();
