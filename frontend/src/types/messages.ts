export default interface IMessage {
  id: number;
  name: string;
  email: string;
  message: string;
  created_at: string;
  user: number;
  status: boolean;
}
