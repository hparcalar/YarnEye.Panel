import { ColorAssignment, ProdLine } from '../models/yarn.models';
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

  async saveProdLine(model: ProdLine) {
      return await this.apiObject.save('ProdLine', model);
  }
  // #endregion

  // #region ASSIGNMENTS
  async getAssignmentList() {
    const data = await this.apiObject.getAll('ColorAssignment');
    return data;
  }

  async getAssignment(id: number) {
    const data = await this.apiObject.get('ColorAssignment', id);
    return data;
  }

  async saveAssignment(model: ColorAssignment) {
      return await this.apiObject.save('ColorAssignment', model);
  }
  // #endregion
}
