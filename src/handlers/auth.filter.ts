export const checkAuthRoute = (router: any, requestedPage: String): boolean => {
    try {
      if (!localStorage.getItem('hyarn_user')) {
        if (requestedPage !== 'login') {
          router.push({ name: 'login' });
          return true;
        }
      }
      else {
        if (requestedPage === 'login') {
          router.push({ name: 'panel' });
          return true;
        }
      }
    }
    catch (err) {
  
    }
  
    return false;
  };
  
  export default checkAuthRoute;
  