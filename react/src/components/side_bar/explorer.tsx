import { Box } from "@mui/material";
import { RichTreeView } from '@mui/x-tree-view/RichTreeView';
import { useState } from 'react';
import { useNavigate } from "react-router-dom";

import type { Tree } from '@/src/lib/types';

import TreeHandler from '@/src/lib/tree_handler';


function Explorer(props: { node_id: string, tree: Tree }) {
  const navigate = useNavigate();
  const [expandedItems, setExpandedItems] = useState<string[]>([]);

  const tree_handler = new TreeHandler(props.tree);
  const parents = tree_handler.getParentNodeIds(props.node_id);
  const displayedExpanded = [
    ...new Set([props.tree.node_id, ...expandedItems, ...parents]),
  ];

  function getItemId(item: Tree) {
    return item.node_id;
  }

  return (
    <>
      <Box >
        <RichTreeView
          sx={{}}
          items={[props.tree]}
          getItemId={getItemId}
          onItemClick={(_, node_id) => {
            navigate(`/main/${node_id}`);
          }}
          selectedItems={props.node_id}
          expandedItems={displayedExpanded}
          onExpandedItemsChange={(_, ids) => setExpandedItems(ids)}
        />
      </Box>
    </>
  );
};

export default Explorer;
