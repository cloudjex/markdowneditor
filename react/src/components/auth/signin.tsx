import {
  Alert, Button, Container, Dialog, DialogActions, DialogTitle, InputLabel, MenuItem, Select, TextField
} from "@mui/material";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

import type { SigninForm, SigninResponse, User, Tree } from "@/src/lib/types";

import RequestHandler from "@/src/lib/request_handler";
import loadingState from "@/src/store/loading_store";
import userStore from '@/src/store/user_store';


function Signin() {
  const navigate = useNavigate();
  const { id_token, setIdToken, user_groups, setUserGroups, setEmail, resetUserState, setTree } = userStore();
  const { setLoading, resetLoadingState } = loadingState();
  const [signinError, setSigninError] = useState(false);
  const { register, handleSubmit, formState: { errors } } = useForm<SigninForm>();

  // 0: null, 1: user group select
  const [dialogKind, setDialogKind] = useState(0);
  const [userGroup, setUserGroup] = useState("");
  const [signinWithGroupError, setSigninWithGroupError] = useState(false);

  useEffect(() => {
    resetUserState();
    resetLoadingState();
  }, []);

  async function onSubmit(data: SigninForm) {
    setLoading(true);
    setSigninError(false);

    const requests = new RequestHandler();
    const signin_res = await requests.post<SigninResponse>(
      `${import.meta.env.VITE_API_HOST}/api/signin`,
      { email: data.email, password: data.password }
    );

    if (signin_res.status != 200) {
      setSigninError(true);
      setLoading(false);
      throw new Error("signin error");
    };

    requests.id_token = signin_res.body.id_token;

    const user_res = await requests.get<User>(
      `${import.meta.env.VITE_API_HOST}/api/users/me`,
    );

    if (user_res.status != 200) {
      setSigninError(true);
      setLoading(false);
      throw new Error("get user info error");
    };

    setLoading(false);
    setUserGroups(user_res.body.user_groups);
    setUserGroup(user_res.body.user_groups[0].group_name);
    setIdToken(signin_res.body.id_token);
    setEmail(data.email);
    setDialogKind(1);
  };

  async function SigninWithUserGroup(user_group: string) {
    if (!user_group) {
      setSigninWithGroupError(true);
      throw new Error("no selected group");
    }

    setDialogKind(0);
    setLoading(true);

    const requests = new RequestHandler(id_token);
    const signin_res = await requests.post<SigninResponse>(
      `${import.meta.env.VITE_API_HOST}/api/signin/group`,
      { user_group: user_group }
    );

    requests.id_token = signin_res.body.id_token;
    const tree_res = await requests.get<Tree>(
      `${import.meta.env.VITE_API_HOST}/api/tree`,
    );

    setLoading(false);
    setIdToken(signin_res.body.id_token);
    setTree(tree_res.body);
    navigate(`/main/${tree_res.body.node_id}`);
  }

  return (
    <>
      <form onSubmit={handleSubmit(onSubmit)}>
        <TextField
          label="メールアドレス"
          fullWidth
          margin="normal"
          {...register("email", {
            required: "メールアドレスは必須です",
          })}
          error={!!errors.email}
          helperText={errors.email?.message}
        />

        <TextField
          label="パスワード"
          type="password"
          fullWidth
          margin="normal"
          {...register("password", {
            required: "パスワードは必須です",
          })}
          error={!!errors.password}
          helperText={errors.password?.message}
        />

        <Button
          type="submit"
          fullWidth
          variant="contained"
          sx={{ mt: 3 }}
        >
          サインイン
        </Button>

        {signinError && (
          <Alert severity="error" sx={{ mt: 2 }}>
            メールアドレスまたはパスワードが正しくありません
          </Alert>
        )}
      </form>

      <Dialog onClose={() => setDialogKind(0)} open={dialogKind == 1}>
        <DialogTitle>
          User Groupを選択してください
        </DialogTitle>

        <Container>
          <InputLabel>User Group</InputLabel>
          <Select
            value={userGroup}
            label="User Group"
            onChange={(e) => setUserGroup(e.target.value as string)}
            sx={{ width: "100%" }}
          >
            {user_groups.map((group) => (
              <MenuItem key={group.group_name} value={group.group_name}>{group.group_name}</MenuItem>
            ))}
          </Select>

          {signinWithGroupError && (
            <Alert severity="error" sx={{ mt: 2 }}>
              User Groupを選択してください
            </Alert>
          )}
        </Container>

        <DialogActions>
          <Button
            autoFocus
            onClick={() => SigninWithUserGroup(userGroup)}
          >
            OK
          </Button>
        </DialogActions>

      </Dialog>
    </>
  );
};

export default Signin;