import { ProdLine } from '../models/yarn.models';
import { ApiGeneric } from './base/api.generic';

export class YarnEyeService {
  apiObject: ApiGeneric = new ApiGeneric();

  // #region PROD LINES
  async getProdLineList() {
    const data = await this.apiObject.getAll('ProdLine');
    return data;
  }

  async getProdLine(id: number) {
    const data = await this.apiObject.get('ProdLine', id);
    return data;
  }

  async saveProcess(model: ProdLine) {
      return await this.apiObject.save('ProdLine', model);
  }
  // #endregion
}
