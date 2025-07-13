export default interface IUser {
  id: number;
  username: string;
  email: string;
  date_joined: string;
}

export default interface IPresenceWs {
  user_id: number;
  name: string;
}

export interface IUserPresence {
  user_id: number;
  name: string;
  is_online: boolean;
}
