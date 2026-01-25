import { Box } from "@mui/material";
import { RichTreeView } from '@mui/x-tree-view/RichTreeView';
import { useState } from 'react';
import { useNavigate } from "react-router-dom";

import type { Tree } from '@/src/lib/types';

import RequestHandler from "@/src/lib/request_handler";
import TreeHandler from '@/src/lib/tree_handler';
import loadingState from "@/src/store/loading_store";
import userStore from "@/src/store/user_store";


function Explorer(props: { node_id: string, tree: Tree }) {
  const navigate = useNavigate();
  const { id_token, setTree } = userStore();
  const { setLoading } = loadingState();
  const [expandedItems, setExpandedItems] = useState<string[]>([]);

  const requests = new RequestHandler(id_token);
  const tree_handler = new TreeHandler(props.tree);
  const parents = tree_handler.getParentNodeIds(props.node_id);
  const displayedExpanded = [
    ...new Set([...expandedItems, ...parents]),
  ];

  async function updateLabel(node_id: string, label: string) {
    setLoading(true);

    const res_promise = requests.put<Tree>(
      `${import.meta.env.VITE_API_HOST}/api/tree/operate/${node_id}`,
      { label: label }
    );
    const res = await res_promise;

    setTree(res.body);
    setLoading(false);
  }

  return (
    <>
      <Box >
        <RichTreeView
          sx={{ backgroundColor: "rgba(245, 245, 245)" }}
          items={[props.tree]}
          onItemClick={(_, id) => {
            navigate(`/main/${id}`);
          }}
          selectedItems={props.node_id}
          expandedItems={displayedExpanded}
          onExpandedItemsChange={(_, ids) => setExpandedItems(ids)}
          isItemEditable
          onItemLabelChange={(itemId, label) => updateLabel(itemId, label)}
        />
      </Box>
    </>
  );
};

export default Explorer;