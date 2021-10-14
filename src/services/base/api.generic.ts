import appConfig from '/config.js';

export class ApiGeneric {
  apiPath: String = appConfig.apiUrl;

  public async get(typeName: String, id: Number) {
    try {
      const responseData = await fetch(`${this.apiPath}${typeName}/${id}`);
      const jsonData = await responseData.json();
      return jsonData;
    } catch (error) {
      
    }
    return null;
  }

  public async getWithParams(typeName: String, params: String[]) {
    let prmString = '';
    params.forEach((d) => {
      prmString += `${d}/`;
    });
    prmString = prmString.substr(0, prmString.length - 1);

    const responseData = await fetch(`${this.apiPath}${typeName}/${prmString}`);
    const jsonData = await responseData.json();
    return jsonData;
  }

  public async getAll(typeName: String) {
    const responseData = await fetch(`${this.apiPath}${typeName}`);
    const jsonData = await responseData.json();
    return jsonData;
  }

  public async save<T>(typeName: String, entity: T) {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(entity),
    };
    const responseData = await fetch(`${this.apiPath}${typeName}`, requestOptions);
    const postId = (await responseData.json()).id;

    return postId;
  }

  public async update<T>(typeName: String, id: number, entity: T) {
    const requestOptions = {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(entity),
    };
    const responseData = await fetch(`${this.apiPath}${typeName}/${id}`, requestOptions);
    const postId = (await responseData.json()).id;

    return postId;
  }

  public delete<T>(entity: T) {

  }
}
