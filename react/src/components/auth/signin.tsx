import {
  Alert, Button, Container, Dialog, DialogActions, DialogTitle, InputLabel, MenuItem, Select, TextField
} from "@mui/material";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

import type { SigninForm, IdToken, Group, Tree } from "@/src/lib/types";

import RequestHandler from "@/src/lib/request_handler";
import loadingState from "@/src/store/loading_store";
import userStore from '@/src/store/user_store';


function Signin() {
  const navigate = useNavigate();
  const { idToken, setIdToken, groups, setGroups, setEmail, resetUserState, setTree } = userStore();
  const { setLoading, resetLoadingState } = loadingState();
  const [signinError, setSigninError] = useState(false);
  const { register, handleSubmit, formState: { errors } } = useForm<SigninForm>();

  // 0: null, 1: user group select
  const [dialogKind, setDialogKind] = useState(0);
  const [stateGroupId, setStateGroupId] = useState("");
  const [signinWithGroupError, setSigninWithGroupError] = useState(false);

  useEffect(() => {
    resetUserState();
    resetLoadingState();
  }, []);

  async function onSubmit(data: SigninForm) {
    setLoading(true);
    setSigninError(false);

    const requests = new RequestHandler();
    const signinRes = await requests.post<IdToken>(
      `/api/signin`,
      { email: data.email, password: data.password }
    );

    if (signinRes.status != 200) {
      setSigninError(true);
      setLoading(false);
      throw new Error("signin error");
    };

    requests.idToken = signinRes.body.id_token;

    const userRes = await requests.get<Group[]>(
      `/api/groups`,
    );

    if (userRes.status != 200) {
      setSigninError(true);
      setLoading(false);
      throw new Error("get groups error");
    };

    setLoading(false);
    setGroups(userRes.body);
    setStateGroupId(userRes.body[0].group_id);
    setIdToken(signinRes.body.id_token);
    setEmail(data.email);
    setDialogKind(1);
  };

  async function signinWithUserGroup(groupId: string) {
    if (!groupId) {
      setSigninWithGroupError(true);
      throw new Error("no selected group");
    }

    setDialogKind(0);
    setLoading(true);

    const requests = new RequestHandler(idToken);
    const signinRes = await requests.post<IdToken>(
      `/api/signin/group`,
      { group_id: groupId }
    );

    requests.idToken = signinRes.body.id_token;
    const treeRes = await requests.get<Tree>(
      `/api/tree`,
    );

    setLoading(false);
    setIdToken(signinRes.body.id_token);
    setTree(treeRes.body);
    navigate(`/node/${treeRes.body.node_id}`);
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
            value={stateGroupId}
            label="User Group"
            onChange={(e) => setStateGroupId(e.target.value)}
            sx={{ width: "100%" }}
          >
            {groups.map((group) => (
              <MenuItem key={group.group_name} value={group.group_id}>{group.group_name}</MenuItem>
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
            onClick={() => signinWithUserGroup(stateGroupId)}
          >
            OK
          </Button>
        </DialogActions>

      </Dialog>
    </>
  );
};

export default Signin;
