import { CognitoUserPool } from 'amazon-cognito-identity-js'

const poolData = {
    UserPoolId: USER_POOL,
    ClientId: CLIENT_ID
}
const UserPool = new CognitoUserPool(poolData)
export default UserPool
