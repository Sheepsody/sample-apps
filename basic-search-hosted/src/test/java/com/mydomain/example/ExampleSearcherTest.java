// Copyright 2018 Yahoo Holdings. Licensed under the terms of the Apache 2.0 license. See LICENSE in the project root.
package com.mydomain.example;

import com.yahoo.component.chain.Chain;
import com.yahoo.search.Query;
import com.yahoo.search.Result;
import com.yahoo.search.Searcher;
import com.yahoo.search.result.Hit;
import com.yahoo.search.searchchain.Execution;
import com.yahoo.search.searchchain.testutil.DocumentSourceSearcher;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

/**
 * Unit test of the example searcher
 */
public class ExampleSearcherTest {

    @Test
    public void testSearcherOnly() {
        Result result = newExecution(new ExampleSearcher()).search(new Query());
        assertEquals("title:hello", result.getQuery().getModel().getQueryTree().toString(),
                     "Query is rewritten");
        assertEquals("test:hit", result.hits().get(0).getId().toString(),
                     "Artificial hit is added");
    }

    @Test
    public void testWithMockBackendProducingHits() {
        DocumentSourceSearcher source = new DocumentSourceSearcher();
        Query mockQuery = new Query("?query=title:hello");
        Result mockResult = new Result(mockQuery);
        mockResult.hits().add(new Hit("hit:1", 0.9));
        mockResult.hits().add(new Hit("hit:2", 0.8));
        mockResult.hits().add(new Hit("hit:3", 0.7));
        source.addResult(mockQuery, mockResult);

        Result result = newExecution(new ExampleSearcher(), source).search(new Query());
        assertEquals("title:hello", result.getQuery().getModel().getQueryTree().toString(),
                     "Query is rewritten");
        assertEquals(4, result.hits().size(),
                     "Artificial hit and document source hits are returned");
    }

    private static Execution newExecution(Searcher... searchers) {
        return new Execution(new Chain<>(searchers), Execution.Context.createContextStub());
    }

}
